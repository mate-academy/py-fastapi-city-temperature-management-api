from app.repositories.city_repository import CityRepository
from app.schemas.city import CityCreate
from fastapi import HTTPException


class CityService:
    def __init__(self, city_repo: CityRepository):
        self.city_repo = city_repo

    async def get_all_cities(self):
        return await self.city_repo.get_all()

    async def create_city(self, city_data: CityCreate):
        return await self.city_repo.create(city_data)

    async def delete_city(self, city_id: int):
        success = await self.city_repo.delete(city_id)
        if not success:
            raise HTTPException(status_code=404, detail="City not found")
        return {"message": "City deleted successfully"}

    async def get_city_by_id(self, city_id: int):
        city = await self.city_repo.get_by_id(city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found")
        return city
