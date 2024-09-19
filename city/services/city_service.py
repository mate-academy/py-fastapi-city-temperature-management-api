import sqlalchemy
from fastapi import HTTPException, status

from city import schemas
from city.repositories.city_repository import CityRepository
from db import models


class CityService:
    def __init__(self, city_repository: CityRepository):
        self.city_repository = city_repository

    async def get_city_by_id(self, city_id: int) -> schemas.City:
        city = await self.city_repository.get_city_by_id(city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found")
        return city

    async def get_cities_list(self) -> list[models.City]:
        return await self.city_repository.get_cities_list()

    async def update_city(self, city_id: int, city: schemas.CityUpdate) -> schemas.City:
        city = await self.city_repository.update_city_by_id(
            city_id,
            city
        )
        if not city:
            raise HTTPException(status_code=404, detail="City not found")
        return city

    async def delete_city(self, city_id: int) -> None:
        result = await self.city_repository.delete_city_by_id(city_id)
        if not result:
            raise HTTPException(status_code=404, detail="City not found")

    async def create_city(self, city: schemas.CityCreate) -> schemas.City:
        try:
            return await self.city_repository.create_city(city)
        except sqlalchemy.exc.SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


