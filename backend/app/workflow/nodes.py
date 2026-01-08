from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import settings
from app.workflow.state import GraphState

# Initialize LLM (Ensure OPENAI_API_KEY is in your .env)
llm = ChatOpenAI(
    model=settings.LLM_MODEL_NAME,
    tiktoken_model_name=settings.TIKTOKEN_MODEL_NAME,
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
    temperature=settings.TEMPERATURE,
)

# --- Component 1: User Query Node ---
# Logic: Validates input and prepares the state.
def node_user_query(state: GraphState) -> GraphState:
    print("--- EXECUTE: USER QUERY NODE ---")
    query = state.get("input_query")
    
    if not query:
        raise ValueError("No input query provided!")
        
    # In the future, you could add query expansion or re-writing here
    return {"input_query": query}


# --- Component 2: LLM Engine Node ---
# Logic: Takes the query (and context later) and generates an answer.
def node_llm_engine(state: GraphState) -> GraphState:
    print("--- EXECUTE: LLM ENGINE NODE ---")
    query = state["input_query"]
    
    # 1. Define the prompt
    # In the future, inject 'context' here for RAG
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant."),
        ("user", "{input}")
    ])
    
    # 2. Chain logic
    chain = prompt | llm
    
    # 3. Invoke
    response = chain.invoke({"input": query})
    
    return {"llm_response": response.content}


# --- Component 3: Output Node ---
# Logic: Formats the final response for the user interface.
def node_output(state: GraphState) -> GraphState:
    print("--- EXECUTE: OUTPUT NODE ---")
    raw_response = state.get("llm_response")
    
    # You might want to format markdown, remove sensitive info, or log chat history here
    return {"final_output": raw_response}