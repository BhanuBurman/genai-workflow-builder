# app/services/embedding_service.py
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_openai import OpenAIEmbeddings
from config import settings

def get_huggingface_embedding_function():
    return HuggingFaceEndpointEmbeddings(
        huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_openai_embedding_function():
    return OpenAIEmbeddings(
        openai_api_key=settings.OPENAI_API_KEY,
        # Common models: "text-embedding-3-small" (cheaper/newer) or "text-embedding-ada-002"
        model="text-embedding-3-small" 
    )