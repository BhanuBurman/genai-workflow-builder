from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.component import Component
from app.schemas.component import ComponentCreate


async def create_component(db: AsyncSession, payload: ComponentCreate) -> Component:
    component = Component(**payload.dict())
    db.add(component)
    await db.commit()
    await db.refresh(component)
    return component


async def get_all_components(db: AsyncSession):
    result = await db.execute(
        select(Component).where(Component.is_active == True)
    )
    return result.scalars().all()


async def get_component_by_type(db: AsyncSession, component_type: str):
    result = await db.execute(
        select(Component).where(Component.type == component_type)
    )
    return result.scalar_one_or_none()
