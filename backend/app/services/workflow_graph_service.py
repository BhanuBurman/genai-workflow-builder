# app/services/workflow_graph_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.workflow import Workflow
from app.models.workflow_node_config import WorkflowNodeConfig
from app.models.component import Component


# =========================
# GET WORKFLOW GRAPH
# =========================
async def get_workflow_graph(db: AsyncSession, workflow_id: int):
    # 1. Fetch Workflow
    result = await db.execute(
        select(Workflow).where(Workflow.id == workflow_id)
    )
    workflow = result.scalar_one_or_none()
    if not workflow:
        return None

    flow_json = workflow.flow_json or {}
    nodes = flow_json.get("nodes", [])
    edges = flow_json.get("edges", [])

    # 2. Fetch Node Configs
    result = await db.execute(
        select(WorkflowNodeConfig).where(
            WorkflowNodeConfig.workflow_id == workflow_id
        )
    )
    node_configs = result.scalars().all()

    node_config_map = {
        cfg.node_id: cfg for cfg in node_configs
    }

    # 3. Fetch Components
    component_types = {cfg.component_type for cfg in node_configs}

    components = []
    if component_types:
        result = await db.execute(
            select(Component).where(Component.type.in_(component_types))
        )
        components = result.scalars().all()

    component_map = {
        c.type: c for c in components
    }

    # 4. Merge node + config + component metadata
    enriched_nodes = []
    for node in nodes:
        node_id = node["id"]
        cfg = node_config_map.get(node_id)
        component = component_map.get(cfg.component_type) if cfg else None

        enriched_nodes.append({
            **node,
            "component": {
                "type": component.type,
                "name": component.name,
                "description": component.description,
                "ui_schema": component.ui_schema
            } if component else None,
            "config": cfg.config_values if cfg else {}
        })

    return {
        "workflow": {
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
        },
        "graph": {
            "nodes": enriched_nodes,
            "edges": edges
        }
    }


# =========================
# SAVE WORKFLOW GRAPH
# =========================
async def save_workflow_graph(db: AsyncSession, workflow_id: int, payload):
    async with db.begin():  # 🔒 atomic transaction
        # 1️⃣ Check if workflow exists
        result = await db.execute(
            select(Workflow).where(Workflow.id == workflow_id)
        )
        workflow = result.scalar_one_or_none()
        if not workflow:
            raise ValueError(f"Workflow with id {workflow_id} not found")

        # 2️⃣ Validate component types
        component_types = {node.type for node in payload.graph.nodes}

        result = await db.execute(
            select(Component.type).where(Component.type.in_(component_types))
        )
        valid_types = set(result.scalars().all())

        invalid = component_types - valid_types
        if invalid:
            raise ValueError(f"Invalid component types: {invalid}")

        # 3️⃣ Prepare flow_json (JSON-safe only)

        # ✅ Nodes → dicts
        flow_nodes = [
            {
                "id": node.id,
                "type": node.type,
                "position": node.position
            }
            for node in payload.graph.nodes
        ]

        # ✅ Edges → dicts (THIS WAS THE BUG)
        flow_edges = [
            {
                "source": edge.source,
                "target": edge.target
            }
            for edge in payload.graph.edges
        ]

        flow_json = {
            "nodes": flow_nodes,
            "edges": flow_edges
        }

        # 4️⃣ Update workflow
        workflow.flow_json = flow_json
        db.add(workflow)

        # 5️⃣ Delete existing node configs
        await db.execute(
            WorkflowNodeConfig.__table__.delete().where(
                WorkflowNodeConfig.workflow_id == workflow_id
            )
        )

        # 6️⃣ Save new node configs
        for node in payload.graph.nodes:
            config = node.data.get("config", {})

            node_config = WorkflowNodeConfig(
                workflow_id=workflow_id,
                node_id=node.id,
                component_type=node.type,
                config_values=config
            )
            db.add(node_config)

        return workflow_id
