class HelloController:
    async def say_hello(self) -> dict:
        return {"message": "Hello from controller!"}