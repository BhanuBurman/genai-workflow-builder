from typing import TypedDict, List, Optional, Any
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    Attributes:
        input_query: The raw query from the user.
        messages: Chat history (for context).
        context: Retrieved documents (for RAG - leaving empty for now).
        llm_response: The raw output from the LLM.
        final_output: The formatted output to send back to the frontend.
    """
    input_query: str
    messages: List[BaseMessage]
    context: Optional[str]
    llm_response: Optional[str]
    final_output: Optional[str]