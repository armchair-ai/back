from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.workflow_step import WorkflowStepListItemResponse
from app.api.dependencies import get_db
from app.services.workflow_step_service import workflow_step_service

router = APIRouter()


@router.get("", response_model=list[WorkflowStepListItemResponse])
@router.get("/", response_model=list[WorkflowStepListItemResponse], include_in_schema=False)
async def get_workflow_steps(
    db: AsyncSession = Depends(get_db),
):
    return await workflow_step_service.get_steps(db, locale="es")
