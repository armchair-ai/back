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

    async def chat_json(
        self,
        prompt: str,
        response_structure: str,
        model: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """
        Solicita al agente procesar la instrucción y responder con la estructura JSON
        especificada en el parámetro 'response_structure'.
        """
        json_prompt = (
            f"{prompt}\n\n"
            "IMPORTANTE: Responde ÚNICAMENTE en formato JSON válido (sin bloques de código markdown) "
            f"con la siguiente estructura exacta:\n{response_structure}"
        )
        
        raw_response = await self.chat(prompt=json_prompt, model=model)
        
        # Extraer el JSON de la respuesta eliminando prefijos de log o bloques markdown
        match_markdown = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
        if match_markdown:
            cleaned = match_markdown.group(1).strip()
        else:
            match_json = re.search(r"\{.*\}", raw_response, re.DOTALL)
            cleaned = match_json.group(0).strip() if match_json else raw_response.strip()
        
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError as err:
            logger.error(f"Error parseando JSON devuelto por el agente: {err}. Respuesta cruda: {raw_response}")
            
        return {
            "success": False,
            "filename": ""
        }


agent_service = AgentService()
