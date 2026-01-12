from app.workflow.state import GraphState
from app.llm_models.embeddings import get_huggingface_embedding_function, get_openai_embedding_function
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config import settings
from langchain_chroma import Chroma

# llm used while development
# llm = ChatOpenAI(
#     model=settings.LLM_MODEL_NAME,
#     tiktoken_model_name=settings.TIKTOKEN_MODEL_NAME,
#     api_key=settings.OPENAI_API_KEY,
#     base_url=settings.OPENAI_BASE_URL,
#     temperature=settings.TEMPERATURE,
# )

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=settings.OPENAI_API_KEY)

NO_RESULTS_FLAG = "__NO_SEARCH_RESULTS__"

# Constants for vector database
CHROMA_PATH = str(settings.CHROMA_DB_PATH)
MAIN_COLLECTION_NAME = "app_knowledge_base"


def node_user_query(state: GraphState) -> GraphState:
    print("--- EXECUTE: USER QUERY ---")
    return {
        "current_content": state["input_query"]
    }


def node_knowledge_base(state: GraphState) -> GraphState:
    print("--- EXECUTE: KNOWLEDGE BASE (RAG) ---")
    
    query = state.get("current_content", "")
    # Optional: State can hold a filter if the user selected a specific file
    filter_filename = state.get("filter_filename", None)
    
    # 1. Initialize Embeddings (Must match ingestion model)
    embedding_function = get_openai_embedding_function()
    ## USING FREE MODEL FOR TESTING
    embedding_function_free = get_huggingface_embedding_function()
    
    # 2. Connect to existing ChromaDB
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
        collection_name=MAIN_COLLECTION_NAME
    )
    
    # 3. Prepare search arguments
    search_kwargs = {}
    if filter_filename:
        print(f"   --- FILTERING BY: {filter_filename} ---")
        search_kwargs["filter"] = {"filename": filter_filename}
    
    # 4. Perform Similarity Search
    # k=3 fetches the top 3 most relevant chunks
    results = vector_store.similarity_search(
        query, 
        k=3,
        **search_kwargs
    )
    
    # 5. Process Results
    if not results:
        print("   No relevant documents found.")
        return {"context": NO_RESULTS_FLAG}
    
    # Combine content from the retrieved docs
    context_text = "\n\n".join([doc.page_content for doc in results])
    
    print(f"   Retrieved {len(results)} chunks.")
    return {"context": context_text}


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
