from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

class GraphState(TypedDict, total=False):
    # Immutable
    input_query: str

    # Baton
    current_content: str

    # RAG sidecar
    context: Optional[str]

    # LLM memory
    messages: List[BaseMessage]

    # Intermediate & final
    llm_response: Optional[str]
    final_output: Optional[str]
