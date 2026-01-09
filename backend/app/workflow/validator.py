from typing import List, Dict, Any, Set
import uuid

# --- Public Error ---
class GraphValidationError(Exception):
    pass


# --- Central Node Registry (single source of truth) ---
NODE_REGISTRY = {
    "userQuery": {
        "role": "start",
        "min_inputs": 0,
        "min_outputs": 1,
    },
    "knowledgeBase": {
        "role": "processor",
        "min_inputs": 1,
        "min_outputs": 1,
    },
    "llm": {
        "role": "processor",
        "min_inputs": 1,
        "min_outputs": 1,
    },
    "output": {
        "role": "end",
        "min_inputs": 1,
        "min_outputs": 0,
    },
}


def validate_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> str:
    """
    Structural graph validation only.
    No execution semantics.
    """

    if not nodes:
        raise GraphValidationError("Graph is empty.")

    node_ids = {n["id"] for n in nodes}
    node_types = {n["id"]: n["type"] for n in nodes}

    # --- 1. Unknown node types ---
    for n in nodes:
        if n["type"] not in NODE_REGISTRY:
            raise GraphValidationError(f"Unknown node type: {n['type']}")

    # --- 2. Build adjacency ---
    adjacency = {nid: set() for nid in node_ids}
    reverse = {nid: set() for nid in node_ids}

    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in node_ids and tgt in node_ids:
            adjacency[src].add(tgt)
            reverse[tgt].add(src)

    # --- 3. Role-based connectivity rules ---
    for node_id, node_type in node_types.items():
        rules = NODE_REGISTRY[node_type]

        if len(reverse[node_id]) < rules["min_inputs"]:
            raise GraphValidationError(
                f"'{node_type}' node requires at least {rules['min_inputs']} input(s)."
            )

        if len(adjacency[node_id]) < rules["min_outputs"]:
            raise GraphValidationError(
                f"'{node_type}' node requires at least {rules['min_outputs']} output(s)."
            )

    # --- 4. Reachability from start ---
    start_nodes = [nid for nid, t in node_types.items() if NODE_REGISTRY[t]["role"] == "start"]
    if not start_nodes:
        raise GraphValidationError("No start node found.")

    visited: Set[str] = set()

    def dfs(nid: str):
        if nid in visited:
            return
        visited.add(nid)
        for nxt in adjacency[nid]:
            dfs(nxt)

    for start in start_nodes:
        dfs(start)

    unreachable = node_ids - visited
    if unreachable:
        raise GraphValidationError(f"Unreachable nodes detected: {unreachable}")

    # --- 5. Soft cycle detection (warn-level future hook) ---
    # NOTE: We ALLOW cycles structurally.
    # Runtime can enforce max-steps / TTL.

    return str(uuid.uuid4())
