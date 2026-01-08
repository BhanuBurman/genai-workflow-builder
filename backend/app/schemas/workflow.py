from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

# Shared properties
class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    flow_json: Dict[str, Any] # Accepts { "nodes": [], "edges": [] }

# Properties to receive on item creation
class WorkflowCreate(WorkflowBase):
    pass

# Properties to return to client
class WorkflowResponse(WorkflowBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)