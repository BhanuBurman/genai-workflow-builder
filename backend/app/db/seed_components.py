from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.component import Component
from app.workflow.components_registry import COMPONENT_DEFINITIONS


async def seed_components(db: AsyncSession):
    for comp in COMPONENT_DEFINITIONS:
        result = await db.execute(
            select(Component).where(Component.type == comp["type"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            continue

        db.add(
            Component(
                name=comp["name"],
                type=comp["type"],
                description=comp["description"],
                ui_schema=comp["ui_schema"],
                handles=comp.get("handles", []),
                is_active=True,
            )
        )

    await db.commit()
