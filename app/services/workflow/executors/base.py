from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseWorkflowExecutor(ABC):
    def _load_system_instructions(self, filename: str) -> Optional[str]:
        if not filename:
            return None
        path = Path("app/workflows/instructions") / Path(filename).name
        return path.read_text(encoding="utf-8") if path.is_file() else None

    @abstractmethod
    async def execute(self, message_id: int) -> None:
        """Execute a specific workflow step for the given message."""
        pass

