from langgraph.graph import StateGraph, END
from app.workflow.state import GraphState
from app.workflow.nodes import node_user_query, node_llm_engine, node_output

# Map Frontend Component Types to Backend Functions
# These keys ("userQuery", "llmEngine") must match the 'type' field in your React Flow JSON
NODE_MAP = {
    "userQuery": node_user_query,
    "llmEngine": node_llm_engine,
    "outputComponent": node_output
}

def build_workflow():
    """
    Constructs the LangGraph workflow.
    For this specific request, we are hardcoding the connection:
    User Query -> LLM Engine -> Output
    """
    workflow = StateGraph(GraphState)

    # 1. Add Nodes
    workflow.add_node("userQuery", node_user_query)
    workflow.add_node("llmEngine", node_llm_engine)
    workflow.add_node("outputComponent", node_output)

    # 2. Define Edges (The Flow)
    # This connects the nodes in a specific order
    workflow.add_edge("userQuery", "llmEngine")
    workflow.add_edge("llmEngine", "outputComponent")
    
    # 3. Set Entry and Exit
    workflow.set_entry_point("userQuery")
    workflow.add_edge("outputComponent", END)

    # 4. Compile
    app = workflow.compile()
    return app