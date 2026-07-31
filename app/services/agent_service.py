from google.antigravity import Agent, LocalAgentConfig


class AgentService:
    async def chat(self, prompt: str, model: str = "gemini-2.5-flash") -> str:
        config = LocalAgentConfig(model=model)
        
        async with Agent(config) as agent:
            response = await agent.chat(prompt)
            return await response.text()


agent_service = AgentService()
