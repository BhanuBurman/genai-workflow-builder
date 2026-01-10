from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from app.db.session import get_db
from app.schemas.workflow import WorkflowResponse, WorkflowCreate
from app.schemas.workflow_graph import (
    WorkflowGraphSaveRequest,
    WorkflowGraphSaveResponse
)
from app.services.workflow_service import create_empty_workflow, get_workflow, get_all_workflows
from app.services.workflow_graph_service import save_workflow_graph

from app.workflow.builder import build_graph_from_frontend
from app.workflow.validator import GraphValidationError
from app.workflow.validator import validate_graph

router = APIRouter()



# --- Schemas ---
class RunGraphRequest(BaseModel):
    message: str                    # The user's question
    nodes: List[Dict[str, Any]]     # React Flow Nodes
    edges: List[Dict[str, Any]]     # React Flow Edges

class WorkflowBuildRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

class WorkflowBuildResponse(BaseModel):
    workflow_id: str
    status: str
    message: str

# --- The NEW Build Endpoint ---
@router.post("/build", response_model=WorkflowBuildResponse)
async def build_workflow(payload: WorkflowBuildRequest):
    """
    Validates the graph structure.
    Does NOT save to DB yet (pure validation).
    Returns a generated workflow_id if successful.
    """
    try:
        # 1. Run Validation Logic
        validate_graph(payload.nodes, payload.edges)
        
        # 2. Return Success
        return {
            "status": "valid",
            "message": "Workflow is valid and ready to run."
        }

    except GraphValidationError as e:
        # 3. Return Logic Error (400 Bad Request)
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # 4. Return Server Error
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@router.post("/run")
async def run_workflow(payload: RunGraphRequest):
    try:
        # 1. Convert Payload to Dict
        graph_data = {"nodes": payload.nodes, "edges": payload.edges}
        
        # 2. Build the Graph
        app_graph = build_graph_from_frontend(graph_data)
        
        # 3. Prepare Input State (The New Contract)
        initial_state = {
            "input_query": payload.message, # The raw history
            "current_content": "",          # Will be set by node_user_query
            "messages": [],
            "context": None,                # Will be set by KB node (if present)
            "final_output": None
        }
        
        # 4. Run Execution
        result = await app_graph.ainvoke(initial_state)
        
        # 5. Return Result
        return {"response": result.get("final_output")}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/")
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
):
    workflow_id = await create_empty_workflow(
        db,
        payload.name,
        payload.description
    )
    return {
        "workflow_id": workflow_id,
        "status": "created"
    }


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def read_workflow(
    workflow_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_workflow = await get_workflow(db, workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

@router.get("/", response_model=List[WorkflowResponse])
async def read_workflows(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await get_all_workflows(db, skip, limit)