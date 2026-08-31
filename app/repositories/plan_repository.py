from app.repositories.base_repository import BaseRepository
from app.models.plan import Plan
from app.schemas.plan import PlanCreate


class PlanRepository(BaseRepository[Plan, PlanCreate]):
    def __init__(self):
        super().__init__(Plan)


plan_repository = PlanRepository()
