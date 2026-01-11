from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate

from app.models.workflow import Workflow
from app.models.workflow_node_config import WorkflowNodeConfig
from app.models.component import Component
from app.services.workflow_graph_service import get_workflow_graph


async def create_empty_workflow(db: AsyncSession, name: str, description: str):
    workflow = Workflow(
        name=name, description=description, flow_json={"nodes": [], "edges": []}
    )
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    return workflow.id


async def run_workflow(db: AsyncSession, workflow_id: int, message: str):
    """
    Run a workflow with the given workflow_id and user message.
    Fetches the workflow graph from DB and executes it.
    """
    from app.workflow.builder import build_graph_from_frontend

    # 1. Fetch workflow
    workflow = await get_workflow(db, workflow_id)
    if not workflow:
        raise ValueError(f"Workflow with id {workflow_id} not found")

    # 2. Get the saved workflow graph
    workflow_graph_data = await get_workflow_graph(db, workflow_id)
    if not workflow_graph_data:
        raise ValueError(f"No workflow graph found for workflow {workflow_id}")

    # 3. Extract nodes and edges from workflow
    graph_data = workflow_graph_data.get("graph", {})
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if not nodes or not edges:
        raise ValueError(f"Workflow {workflow_id} has no nodes or edges")

    # 4. Build the LangGraph from the saved workflow
    flow_dict = {"nodes": nodes, "edges": edges}
    app_graph = build_graph_from_frontend(flow_dict)

    # 5. Prepare initial state with user message
    initial_state = {
        "input_query": message,
        "current_content": "",
        "messages": [],
        "context": None,
        "final_output": None,
    }

    # 6. Execute the workflow graph
    result = await app_graph.ainvoke(initial_state)

    # 7. Return the final output
    return result.get("final_output")


async def get_workflow(db: AsyncSession, workflow_id: int):
    result = await db.execute(select(Workflow).filter(Workflow.id == workflow_id))
    return result.scalars().first()


async def get_all_workflows(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Workflow).offset(skip).limit(limit))
    return result.scalars().all()
