from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import ModelNotFoundError
from app.controllers.file_controller import FileController
from app.api.endpoints import orders, messages
from app.middlewares.request_logger_middleware import RequestLoggerMiddleware


app = FastAPI()

app.add_middleware(RequestLoggerMiddleware)

@app.exception_handler(ModelNotFoundError)
async def model_not_found_exception_handler(request: Request, exc: ModelNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )

""" file_controller = FileController()

@app.get("/")
async def root():
    return await file_controller.get_files_info() """

app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(messages.router, tags=["Messages"])