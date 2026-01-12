# app/models/__init__.py

# 1. Import Base so we can access it as 'models.Base'
from app.db.session import Base

# 2. Import all your models here
# This registers them with Base.metadata so create_all() finds them!
from app.models.workflow import Workflow
from app.models.component import Component
from app.models.workflow_node_config import WorkflowNodeConfig
from app.models.file import File
# from app.models.document import Document