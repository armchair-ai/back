from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.exceptions import ModelNotFoundError
from app.controllers.file_controller import FileController
from app.api.endpoints import orders, messages, workflow_steps
from app.middlewares.request_logger_middleware import RequestLoggerMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggerMiddleware)

@app.exception_handler(ModelNotFoundError)
async def model_not_found_exception_handler(request: Request, exc: ModelNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )

app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(messages.router, tags=["Messages"])
app.include_router(workflow_steps.router, prefix="/steps", tags=["Workflow Steps"])
