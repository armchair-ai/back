import logging
from typing import Any, Dict, Optional
from google.antigravity import Agent, LocalAgentConfig

logger = logging.getLogger(__name__)


class AgentService:
    async def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_instructions: Optional[str] = None,
    ) -> str:
        config = LocalAgentConfig(
            model=model or "gemini-2.5-flash",
            system_instructions=system_instructions,
        )
        
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            return await response.text()

    async def chat_structured(
        self,
        prompt: str,
        response_structure: Any,
        model: Optional[str] = None,
        system_instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        config = LocalAgentConfig(
            model=model or "gemini-2.5-flash",
            response_schema=response_structure,
            system_instructions=system_instructions,
        )
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            return await response.structured_output()

    async def chat_structured_with_text(
        self,
        prompt: str,
        response_structure: Any,
        model: Optional[str] = None,
        system_instructions: Optional[str] = None,
    ) -> tuple[Optional[Dict[str, Any]], str]:
        config = LocalAgentConfig(
            model=model or "gemini-2.5-flash",
            response_schema=response_structure,
            system_instructions=system_instructions,
        )
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            structured = await response.structured_output()
            text = await response.text()
            return structured, text

agent_service = AgentService()
