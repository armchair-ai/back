from fastapi import FastAPI
from app.controllers.file_controller import FileController

app = FastAPI()
file_controller = FileController()

@app.get("/")
async def root():
    return await file_controller.get_files_info()