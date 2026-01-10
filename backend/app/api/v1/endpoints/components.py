from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List

from app.db.session import get_db
from app.schemas.component import ComponentCreate, ComponentResponse
from app.services import component_service

router = APIRouter()

class ComponentShortResponse(BaseModel):
    id: int
    name: str
    description: str
    ui_schema: Dict[str, Any]
    is_active: bool

@router.post("/", response_model=ComponentResponse)
async def create_component(
    payload: ComponentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await component_service.create_component(db, payload)


@router.get("/", response_model=List[ComponentShortResponse])
async def list_components(db: AsyncSession = Depends(get_db)):
    components = await component_service.get_all_components(db)
    return [ComponentShortResponse(
        id=component.id,
        name=component.name,
        description=component.description,
        ui_schema=component.ui_schema,
        is_active=component.is_active
    ) for component in components]


@router.get("/{component_type}", response_model=ComponentResponse)
async def get_component(component_type: str, db: AsyncSession = Depends(get_db)):
    component = await component_service.get_component_by_type(db, component_type)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return component
