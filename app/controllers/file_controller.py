from app.services.agent_service import agent_service


class FileController:
    async def get_files_info(self) -> dict:
        model = "gemini-2.5-flash"
        prompt = "What files are in the current directory?"
        response_text = await agent_service.chat(prompt=prompt, model=model)
            
        return {
            "status": "success",
            "model_used": model,
            "agent_response": response_text
        }