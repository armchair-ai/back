import json
import logging
import re
from typing import Any, Dict
from google.antigravity import Agent, LocalAgentConfig

logger = logging.getLogger(__name__)


class AgentService:
    async def chat(self, prompt: str, model: str = "gemini-2.5-flash") -> str:
        """
        Envía un prompt al agente y retorna la respuesta en texto plano.
        """
        config = LocalAgentConfig(model=model)
        
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            return await response.text()

    async def chat_structured(
        self,
        prompt: str,
        response_structure: Any,
        model: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        config = LocalAgentConfig(
            model=model,
            response_schema=response_structure
        )
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            return await response.structured_output()

agent_service = AgentService()
