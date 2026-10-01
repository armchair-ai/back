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
            "system_instructions": "create_plan/system_instructions.md",
            "response_schema": "PlannerResponse",
            "skills_paths": "skills",
        }
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
            print(f"  [=] WorkflowStep '{data['name']}' ya existe, omitiendo.")
