from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.db.session import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    # Workflow ID (required - files are associated with a workflow from upload)
    workflow_id = Column(Integer, nullable=False, index=True)

    # Original filename
    filename = Column(String(255), nullable=False)

    # File path in user_files folder
    filepath = Column(String(512), nullable=False)

    # File size in bytes
    size = Column(Integer, nullable=False)

    # MIME type (e.g., application/pdf, image/png)
    content_type = Column(String(100), nullable=True)

    # Timestamp when file was uploaded
    uploaded_at = Column(DateTime, server_default=func.now())

    # NEW: Track if document is ingested in vector DB
    is_ingested = Column(Boolean, default=False)
    ingested_at = Column(DateTime, nullable=True)
