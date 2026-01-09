from langgraph.graph import StateGraph, END
from app.workflow.state import GraphState
from app.workflow.nodes import (
    node_user_query,
    node_knowledge_base,
    node_llm_engine,
    node_output
)

NODE_MAP = {
    "userQuery": node_user_query,
    "knowledgeBase": node_knowledge_base,
    "llm": node_llm_engine,
    "output": node_output,
}

def build_graph_from_frontend(flow: dict):
    workflow = StateGraph(GraphState)

    nodes = flow["nodes"]
    edges = flow["edges"]

    for n in nodes:
        workflow.add_node(n["id"], NODE_MAP[n["type"]])

    for e in edges:
        workflow.add_edge(e["source"], e["target"])

    # Entry = userQuery
    entry = next(n["id"] for n in nodes if n["type"] == "userQuery")
    workflow.set_entry_point(entry)

    # END only from output nodes
    for n in nodes:
        if n["type"] == "output":
            workflow.add_edge(n["id"], END)

    return workflow.compile()
