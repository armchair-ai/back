import asyncio
from app.core.database import AsyncSessionLocal
from database.seeds import workflow_steps


async def main() -> None:
    """Run all database seeders."""
    print("Iniciando seeders de base de datos...")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            print("Ejecutando workflow_steps seeder...")
            await workflow_steps.seed(session)
    print("Seeding completado con éxito.")


if __name__ == "__main__":
    asyncio.run(main())
