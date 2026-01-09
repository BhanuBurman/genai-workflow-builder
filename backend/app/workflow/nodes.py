from app.workflow.state import GraphState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config import settings

llm = ChatOpenAI(
    model=settings.LLM_MODEL_NAME,
    tiktoken_model_name=settings.TIKTOKEN_MODEL_NAME,
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
    temperature=settings.TEMPERATURE,
)

NO_RESULTS_FLAG = "__NO_SEARCH_RESULTS__"

def node_user_query(state: GraphState) -> GraphState:
    print("--- EXECUTE: USER QUERY ---")
    return {
        "current_content": state["input_query"]
    }

def node_knowledge_base(state: GraphState) -> GraphState:
    print("--- EXECUTE: KNOWLEDGE BASE ---")
    query = state.get("current_content", "")

    if "pricing" in query.lower():
        return {"context": "Pricing is $10/mo."}

    return {"context": NO_RESULTS_FLAG}

def node_llm_engine(state: GraphState) -> GraphState:
    print("--- EXECUTE: LLM ENGINE ---")

    query = state.get("current_content", "")
    context = state.get("context")
    existing = state.get("llm_response")

    # RAG success
    if context and context != NO_RESULTS_FLAG:
        prompt = ChatPromptTemplate.from_template(
            "Answer ONLY using this context:\n{context}\n\nQuestion: {input}"
        )
        return {
            "llm_response": (prompt | llm).invoke(
                {"context": context, "input": query}
            ).content
        }

    # RAG failed
    if context == NO_RESULTS_FLAG:
        if existing:
            return {}
        return {
            "llm_response": "I checked the Knowledge Base but couldn’t find relevant information."
        }

    # General chat
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Question: {input}"
    )
    return {
        "llm_response": (prompt | llm).invoke({"input": query}).content
    }

def node_output(state: GraphState) -> GraphState:
    return {
        "final_output": state.get("llm_response")
    }
