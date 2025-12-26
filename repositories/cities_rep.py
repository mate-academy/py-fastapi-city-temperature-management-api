from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CityModel
from database.sqlite import get_context
from schemas.cities_schema import CityCreateSchema, CityResponseSchema, CityListSchema


async def get_city_rep():
    async with get_context() as session:
        yield CityRep(session)


class CityRep:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_city(self, city_data: CityCreateSchema):
        city = CityModel(
            name=city_data.name,
            additional_info=city_data.additional_info
        )
        self.session.add(city)
        await self.session.commit()
        await self.session.refresh(city)

        return CityResponseSchema.model_validate(city)


    async def update_city(self, city_id, city_data: CityCreateSchema):
        result = await self.session.execute(select(CityModel).where(CityModel.id == city_id))

        city = result.scalar_one_or_none()
        if not city:
            raise HTTPException(status_code=404, detail=f"City with {city_id} not found")

        city.name = city_data.name
        city.additional_info = city_data.additional_info

        await self.session.commit()

        return {"detail": "Successful changed"}


    async def get_cities(self):
        result = await self.session.execute(select(CityModel))

        cities = result.scalars().all()
        cities = [CityResponseSchema.model_validate(city) for city in cities]

        return CityListSchema(cities=cities)


    async def get_city(self, city_id):
        result = await self.session.execute(select(CityModel).where(CityModel.id == city_id))
        city = result.scalar_one_or_none()

        if not city:
            raise HTTPException(status_code=404, detail=f"City {city_id} not found")

        return CityResponseSchema.model_validate(city)


    async def remove_city(self, city_id):
        result = await self.session.execute(select(CityModel).where(CityModel.id == city_id))
        city = result.scalar_one_or_none()
        if not city:
            raise HTTPException(status_code=404, detail=f"City {city_id} not found")

        await self.session.delete(city)
        await self.session.commit()

        return {"detail": f"City {city_id} deleted"}
