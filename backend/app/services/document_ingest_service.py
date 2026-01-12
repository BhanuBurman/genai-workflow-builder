import os
from app.llm_models.embeddings import get_huggingface_embedding_function
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from config import settings

CHROMA_PATH = str(settings.CHROMA_DB_PATH)
MAIN_COLLECTION_NAME = "app_knowledge_base"

# embedding_function = OpenAIEmbeddings(
#     model=settings.EMBEDDING_MODEL_NAME,
#     base_url=settings.OPENAI_BASE_URL,
#     api_key=settings.OPENAI_API_KEY,
#     tiktoken_model_name=settings.EMBEDDING_TIKTOKEN_MODEL_NAME,
# )


embedding_function = get_huggingface_embedding_function()

async def ingest_pdf_to_vector_db(file_path: str, filename: str):
    """
    Loads PDF, chunks it, and stores in Chroma with metadata.

    Args:
        file_path: Full path to the PDF file
        filename: Original filename for metadata

    Returns:
        True if successful

    Raises:
        Exception: If ingestion fails
    """
    try:
        print(f"--- INGESTING: {filename} into {MAIN_COLLECTION_NAME} ---")

        # 1. Load PDF
        loader = PyMuPDFLoader(file_path)
        docs = loader.load()

        # 2. Add metadata to each document
        for doc in docs:
            doc.metadata["filename"] = filename
            doc.metadata["file_path"] = file_path

        # 3. Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        if not splits:
            print(f"--- WARNING: No content extracted from {filename} ---")
            return False

        # 4. Save to Chroma with embeddings
        Chroma.from_documents(
            documents=splits,
            embedding=embedding_function,
            persist_directory=CHROMA_PATH,
            collection_name=MAIN_COLLECTION_NAME,
        )

        print(f"--- SUCCESS: Added {len(splits)} chunks from {filename} ---")
        return True

    except Exception as e:
        print(f"--- INGESTION ERROR for {filename}: {str(e)} ---")
        raise
