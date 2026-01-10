# app/api/workflow_graph.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.workflow_graph import WorkflowGraphResponse
from app.schemas.workflow_graph import WorkflowGraphSaveRequest
from app.services.workflow_graph_service import get_workflow_graph
from app.services.workflow_graph_service import save_workflow_graph

router = APIRouter()


@router.get("/{workflow_id}/graph", response_model=WorkflowGraphResponse)
async def get_workflow_graph_api(
    workflow_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await get_workflow_graph(db, workflow_id)
    if not result:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return result

@router.patch("/{workflow_id}")
async def save_workflow_graph_api(
    workflow_id: int,
    payload: WorkflowGraphSaveRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        await save_workflow_graph(db, workflow_id, payload)
        return {"status": "saved"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

