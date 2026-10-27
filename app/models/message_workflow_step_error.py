from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base


class MessageWorkflowStepError(Base):
    __tablename__ = "message_workflow_step_errors"

    id = Column(Integer, primary_key=True, index=True)
    message_workflow_step_id = Column(Integer, ForeignKey("message_workflow_steps.id", ondelete="CASCADE"), nullable=False, index=True)
    error_message = Column(Text, nullable=False)
    error_traceback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    message_workflow_step = relationship("MessageWorkflowStep", back_populates="errors")
