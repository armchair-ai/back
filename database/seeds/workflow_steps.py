from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workflow_step import WorkflowStep


async def seed(session: AsyncSession) -> None:
    """Seed initial workflow steps."""
    initial_steps: list[dict[str, object]] = [
        {
            "name": "create_plan",
            "order": 1,
            "model": "gemini-2.5-flash",
            "system_instructions": "create_plan.md",
            "response_schema": "PlannerResponse",
            "skills_paths": "skills",
        },
        {
            "name": "execute_plan",
            "order": 2,
            "model": "gemini-2.5-flash",
            "system_instructions": "execute_plan.md",
            "response_schema": "ExecutePlanResponse",
            "skills_paths": "skills",
        },
        # {
        #     "name": "review_code_style",
        #     "order": 3,
        #     "model": "gemini-2.5-flash",
        #     "system_instructions": "review_code_style.md",
        #     "response_schema": None,
        #     "skills_paths": "skills",
        # },
    ]

    for data in initial_steps:
        query = select(WorkflowStep).where(WorkflowStep.name == data["name"])
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if not existing:
            step = WorkflowStep(**data)
            session.add(step)
            print(f"  [+] WorkflowStep '{data['name']}' creado.")
        else:
            # Actualizar campos existentes para mantener sincronizada la configuración
            for key, val in data.items():
                setattr(existing, key, val)
            print(f"  [=] WorkflowStep '{data['name']}' actualizado.")
