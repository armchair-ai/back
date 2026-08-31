from pydantic import BaseModel
from app.events.message import MessageCreatedEvent
from app.core.database import AsyncSessionLocal
from app.repositories.message_repository import message_repository
from app.repositories.plan_repository import plan_repository
from app.schemas.plan import PlanCreate
from app.services.agent_service import agent_service
from app.core.event_dispatcher import event_dispatcher


async def create_plan_listener(event: BaseModel) -> None:
    """
    Listener que reacciona a MessageCreatedEvent, consulta el mensaje en la BD,
    ejecuta el agente para generar un plan y persiste el registro en la tabla plans.
    """
    if isinstance(event, MessageCreatedEvent):
        async with AsyncSessionLocal() as db:
            message = await message_repository.get(db, id=event.id)
            if not message:
                return

            response_structure = '{\n  "success": true,\n  "filename": "nombre_del_archivo.md"\n}'
            agent_result = await agent_service.chat_json(
                prompt=message.text,
                response_structure=response_structure
            )
            
            is_success = agent_result.get("success", False)
            filename = str(agent_result.get("filename", "")).strip()
            
            if is_success and filename:
                plan = PlanCreate(filename=filename, message_id=message.id)
                await plan_repository.create(db, obj_in=plan)


event_dispatcher.register(create_plan_listener)
