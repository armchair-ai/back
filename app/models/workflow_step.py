from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    system_instructions = Column(String, nullable=False)
    response_schema = Column(String, nullable=True)
    skills_paths = Column(String, nullable=True)

    message_workflow_steps = relationship("MessageWorkflowStep", back_populates="workflow_step", cascade="all, delete-orphan")
