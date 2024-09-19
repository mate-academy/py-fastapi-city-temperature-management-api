from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from db import models


class CityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cities_list(self) -> [schemas.City]:
        query = select(models.City)
        cities_list = await self.session.execute(query)
        return [
            schemas.City.model_validate(city[0])
            for city in cities_list.fetchall()
        ]

    async def get_city_by_id(self, city_id: int) -> schemas.City | None:
        query = select(models.City).where(models.City.id == city_id)
        result = await self.session.execute(query)
        db_city = result.scalar_one_or_none()
        if db_city:
            return schemas.City.model_validate(db_city)

    async def update_city_by_id(
        self,
        city_id: int,
        city: schemas.CityUpdate,
    ) -> schemas.City | None:
        async with self.session.begin():
            query = select(models.City).where(models.City.id == city_id)

            result = await self.session.execute(query)
            db_city = result.scalar_one_or_none()

            if not db_city:
                return None

            db_city.name = city.name
            db_city.additional_info = city.additional_info

        await self.session.refresh(db_city)
        return schemas.City.model_validate(db_city)

    async def create_city(
        self,
        city: schemas.CityCreate
    ) -> schemas.City:
        db_city = models.City(
            name=city.name,
            additional_info=city.additional_info
        )
        async with self.session.begin():
            self.session.add(db_city)

        await self.session.refresh(db_city)

        return schemas.City.model_validate(db_city)

    async def delete_city_by_id(self, city_id: int) -> bool:
        async with self.session.begin():
            query = select(models.City).where(models.City.id == city_id)
            result = await self.session.execute(query)
            db_city = result.scalar_one_or_none()
            if not db_city:
                return False
            await self.session.delete(db_city)

        return True
