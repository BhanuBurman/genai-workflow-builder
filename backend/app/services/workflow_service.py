from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate

async def create_workflow(db: AsyncSession, workflow: WorkflowCreate):
    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        flow_json=workflow.flow_json
    )
    db.add(db_workflow)
    await db.commit()
    await db.refresh(db_workflow)
    return db_workflow

async def get_workflow(db: AsyncSession, workflow_id: int):
    result = await db.execute(select(Workflow).filter(Workflow.id == workflow_id))
    return result.scalars().first()

async def get_all_workflows(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Workflow).offset(skip).limit(limit))
    return result.scalars().all()