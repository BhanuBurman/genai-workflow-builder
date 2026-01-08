from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_path = Column(String) # Path to local storage or S3 URL
    collection_name = Column(String) # For ChromaDB collection reference
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())