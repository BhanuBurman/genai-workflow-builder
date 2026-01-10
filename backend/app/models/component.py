from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, func
from app.db.session import Base


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)

    # Display name shown in UI
    name = Column(String(100), nullable=False)

    # Unique key used by frontend & backend (llm, knowledgeBase, output)
    type = Column(String(50), unique=True, nullable=False)

    # Description shown in UI
    description = Column(String(255), nullable=True)

    ui_schema = Column(JSON, nullable=True)

    # Store handle configuration per component type
    handles = Column(JSON, nullable=False, default=list)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
