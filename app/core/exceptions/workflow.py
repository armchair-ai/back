from app.core.exceptions.base import DomainException


class WorkflowExecutionError(DomainException):
    """Exception raised when a workflow step execution fails."""
    def __init__(self, message: str = "Workflow step execution failed"):
        self.message = message
        super().__init__(self.message)


class ArtifactNotFoundError(WorkflowExecutionError):
    """Exception raised when an expected artifact (plan, summary, etc.) is missing or cannot be resolved."""
    pass
