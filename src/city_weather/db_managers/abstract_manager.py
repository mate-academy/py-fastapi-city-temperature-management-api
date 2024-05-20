from abc import ABC, abstractmethod
from sqlalchemy import select
from src.database import SessionLocal


class AbstractDBManager(ABC):
    model = None

    async def get_list_of_items(self):
        async with SessionLocal() as session:
            return await session.scalars(select(self.model))

    @abstractmethod
    async def update_item(self, *args, **kwargs):
        pass


