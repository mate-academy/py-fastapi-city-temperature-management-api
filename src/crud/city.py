import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.config.settings import get_settings
from src.models.city import CityModel
from src.schemas.city import CityRequestSchema, CityTemperatureResponseSchema


class CityService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()

    async def create_city(self, city: CityRequestSchema) -> CityTemperatureResponseSchema:
        try:
            city_db = CityModel(name=city.name, additional_info=city.additional_info)
            self.db.add(city_db)
            await self.db.commit()
            return CityTemperatureResponseSchema.model_validate(city_db)

        except Exception:
            await self.db.rollback()
            raise

    async def fetch_and_save_ukraine_cities(self) -> None:
        url = "https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            cities = response.json()
        ukraine_cities = [c for c in cities if c["country"] == "UA"][:30]

        for city in ukraine_cities:
            exists = await self.db.scalar(select(CityModel).where(CityModel.name == city["name"]))
            if exists:
                continue
            db_city = CityModel(name=city["name"], additional_info=f"country: {city.get('country', '')}")
            self.db.add(db_city)
        await self.db.commit()

    async def get_cities(self) -> list[CityModel]:
        result = await self.db.scalars(
            select(CityModel).options(selectinload(CityModel.temperature))
        )
        return list(result.all())

    async def get_city(self, city_id: int) -> CityModel | None:
        city = await self.db.scalar(
            select(CityModel)
            .where(CityModel.id == city_id)
            .options(joinedload(CityModel.temperature))
        )
        return city

    async def update_city(self, city_id: int, city: CityRequestSchema) -> CityModel:
        try:
            city_db = await self.db.scalar(select(CityModel).where(CityModel.id == city_id))
            if city_db:
                update_data = city.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(city_db, key, value)
                await self.db.commit()
                await self.db.refresh(city_db)
            return city_db
        except Exception:
            await self.db.rollback()
            raise

    async def delete_city(self, city_id: int) -> CityModel | None:
        city_db = await self.db.scalar(select(CityModel).where(CityModel.id == city_id))
        if city_db:
            await self.db.delete(city_db)
            await self.db.commit()
        return city_db
