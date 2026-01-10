from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate

from app.models.workflow import Workflow
from app.models.workflow_node_config import WorkflowNodeConfig
from app.models.component import Component


async def create_empty_workflow(db: AsyncSession, name: str, description: str):
    workflow = Workflow(
        name=name,
        description=description,
        flow_json={"nodes": [], "edges": []}
    )
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return workflow.id

async def get_workflow(db: AsyncSession, workflow_id: int):
    result = await db.execute(select(Workflow).filter(Workflow.id == workflow_id))
    return result.scalars().first()

async def get_all_workflows(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Workflow).offset(skip).limit(limit))
    return result.scalars().all()

