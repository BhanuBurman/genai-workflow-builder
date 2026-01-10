from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class HandleSchema(BaseModel):
    id: str
    type: str  # "source" | "target"
    position: str  # "top" | "bottom" | "left" | "right"


class ComponentBase(BaseModel):
    name: str
    type: str
    description: str
    ui_schema: Dict[str, Any]
    handles: List[HandleSchema] = []
    is_active: bool = True


class ComponentCreate(ComponentBase):
    pass


class ComponentResponse(ComponentBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
