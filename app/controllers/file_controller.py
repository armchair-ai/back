from google.antigravity import Agent, LocalAgentConfig

class FileController:
    async def get_files_info(self) -> dict:
        # Especificamos explícitamente un modelo soportado en v1beta (ej. gemini-2.5-flash o gemini-3.5-flash)
        config = LocalAgentConfig(model="gemini-2.5-flash")
        
        async with Agent(config) as agent:
            response = await agent.chat("What files are in the current directory?")
            response_text = await response.text()
            
        return {
            "status": "success",
            "model_used": "gemini-2.5-flash",
            "agent_response": response_text
        }