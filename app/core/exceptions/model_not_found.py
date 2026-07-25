from app.core.exceptions.base import DomainException

class ModelNotFoundError(DomainException):
    """Exception raised when a requested model/entity is not found in the database."""
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)
