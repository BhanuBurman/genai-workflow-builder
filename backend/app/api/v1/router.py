from fastapi import APIRouter
from app.api.v1.endpoints import workflows
from app.api.v1.endpoints import components
from app.api.v1.endpoints import workflow_graph

api_router = APIRouter()
api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
api_router.include_router(components.router, prefix="/components", tags=["Components"])
api_router.include_router(workflow_graph.router, prefix="/workflow-graph", tags=["Workflow Graph"])
# api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])