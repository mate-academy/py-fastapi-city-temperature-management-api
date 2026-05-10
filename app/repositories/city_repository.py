from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.city import DBCity
from app.schemas.city import CityCreate
from typing import Sequence


class CityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[DBCity]:
        result = await self.session.execute(select(DBCity))
        return result.scalars().all()

    async def create(self, city_data: CityCreate) -> DBCity:
        new_city = DBCity(
            name=city_data.name,
            additional_info=city_data.additional_info
        )
        self.session.add(new_city)
        await self.session.commit()
        await self.session.refresh(new_city)
        return new_city

    async def delete(self, city_id: int) -> bool:
        city = await self.session.get(DBCity, city_id)
        if city:
            await self.session.delete(city)
            await self.session.commit()
            return True
        return False

    async def get_by_id(self, city_id: int) -> DBCity | None:
        return await self.session.get(DBCity, city_id)
