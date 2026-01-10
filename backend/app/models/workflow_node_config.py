from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.db.session import Base


class WorkflowNodeConfig(Base):
    __tablename__ = "workflow_node_configs"

    id = Column(Integer, primary_key=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
    )

    # React Flow node id
    node_id = Column(String, nullable=False)

    # Component type (llm, knowledgeBase, etc.)
    component_type = Column(String, nullable=False)

    # User-filled values ONLY
    config_values = Column(JSON, nullable=False)

    # Handle configuration (ports)
    handles = Column(JSON, nullable=False, default=list)
