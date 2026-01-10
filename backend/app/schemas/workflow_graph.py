# app/schemas/workflow_graph.py
from pydantic import BaseModel
from typing import Any, Dict, List

class NodeInput(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, Any]


class EdgeInput(BaseModel):
    source: str
    target: str


class GraphInput(BaseModel):
    nodes: List[NodeInput]
    edges: List[EdgeInput]


class WorkflowMetaInput(BaseModel):
    name: str
    description: str

class WorkflowMeta(BaseModel):
    id: int
    name: str
    description: str

class WorkflowGraphResponse(BaseModel):
    graph: Dict[str, Any]


class WorkflowGraphSaveRequest(BaseModel):
    graph: GraphInput


class WorkflowGraphSaveResponse(BaseModel):
    workflow_id: int
    status: str
