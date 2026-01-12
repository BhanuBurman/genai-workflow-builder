# app/services/embedding_service.py
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from config import settings

def get_huggingface_embedding_function():
    return HuggingFaceEndpointEmbeddings(
        huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )