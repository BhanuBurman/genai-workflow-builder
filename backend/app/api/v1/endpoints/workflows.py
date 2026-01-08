from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.services import workflow_service

from app.workflow.builder import build_workflow

router = APIRouter()


class RunRequest(BaseModel):
    message: str

@router.post("/run")
async def run_workflow_endpoint(request: RunRequest):
    # 1. Initialize the Graph
    workflow_app = build_workflow()
    
    # 2. Define Initial State
    initial_state = {
        "input_query": request.message,
        "messages": [],
        "context": None,
        "llm_response": None,
        "final_output": None
    }
    
    # 3. Invoke the Graph
    # Use ainvoke for async execution
    try:
        result = await workflow_app.ainvoke(initial_state)
        return {"response": result["final_output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    workflow: WorkflowCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await workflow_service.create_workflow(db, workflow)

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def read_workflow(
    workflow_id: int, 
    db: AsyncSession = Depends(get_db)
):
    db_workflow = await workflow_service.get_workflow(db, workflow_id)
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

@router.get("/", response_model=List[WorkflowResponse])
async def read_workflows(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    return await workflow_service.get_all_workflows(db, skip, limit)