from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any, Dict, List, Optional
from datetime import datetime

from app.db.session import get_db
from app.schemas.workflow import WorkflowResponse, WorkflowCreate
from app.schemas.workflow_graph import (
    WorkflowGraphSaveRequest,
    WorkflowGraphSaveResponse,
)
from app.services.workflow_service import (
    create_empty_workflow,
    get_workflow,
    get_all_workflows,
    run_workflow as run_workflow_service,
)
from app.services.workflow_graph_service import save_workflow_graph
from app.services.document_ingest_service import ingest_pdf_to_vector_db
from app.models.file import File

from app.workflow.builder import build_graph_from_frontend
from app.workflow.validator import GraphValidationError
from app.workflow.validator import validate_graph

router = APIRouter()


# --- Schemas ---
class RunGraphRequest(BaseModel):
    workflow_id: int  # The workflow to run
    message: str  # The user's question


class WorkflowBuildRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    workflow_id: int  # Required: for ingesting files


class WorkflowBuildResponse(BaseModel):
    status: str
    message: str


# --- The NEW Build Endpoint ---
@router.post("/build", response_model=WorkflowBuildResponse)
async def build_workflow(
    payload: WorkflowBuildRequest, db: AsyncSession = Depends(get_db)
):
    """
    Validates the graph structure AND ingests documents to vector DB.
    """
    try:
        # 1. Run Validation Logic
        validate_graph(payload.nodes, payload.edges)

        # 2. NEW: Ingest documents from workflow files
        # Fetch all files associated with this workflow
        stmt = select(File).where(File.workflow_id == payload.workflow_id)
        result = await db.execute(stmt)
        files = result.scalars().all()

        for file in files:
            if not file.is_ingested:  # Only ingest if not already done
                try:
                    await ingest_pdf_to_vector_db(file.filepath, file.filename)
                    # Update file record
                    file.is_ingested = True
                    file.ingested_at = datetime.utcnow()
                    db.add(file)
                except Exception as ingest_error:
                    print(
                        f"Warning: Failed to ingest {file.filename}: {str(ingest_error)}"
                    )

        await db.commit()

        # 3. Return Success
        return {"status": "valid", "message": "Build Successful"}

    except GraphValidationError as e:
        # 4. Return Logic Error (400 Bad Request)
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # 5. Return Server Error
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")


@router.post("/run")
async def run_workflow(payload: RunGraphRequest, db: AsyncSession = Depends(get_db)):
    """
    Run a workflow with the specified workflow_id and user message.
    Fetches the saved workflow graph from DB and executes it.
    """
    try:
        # 1. Call the workflow service to run the workflow
        result = await run_workflow_service(db, payload.workflow_id, payload.message)

        # 2. Return Result
        return {"response": result}

    except ValueError as e:
        # Workflow not found or invalid
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
):
    workflow_id = await create_empty_workflow(db, payload.name, payload.description)
    return {"workflow_id": workflow_id, "status": "created"}


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def read_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    db_workflow = await get_workflow(db, workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow


@router.get("/", response_model=List[WorkflowResponse])
async def read_workflows(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await get_all_workflows(db, skip, limit)
