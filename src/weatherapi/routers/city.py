from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.weatherapi.crud.city import create_city, delete_city_by_id, get_city_list_pagination
from src.weatherapi.schemas.city import CityRead, CityCreate, CityReadWithTemperatures

city_router = APIRouter()


@city_router.post("/cities/", response_model=CityRead)
async def new_city(city_data: CityCreate, session: AsyncSession = Depends(get_session)):
    return await create_city(city_in=city_data, session=session)


@city_router.get("/cities/", response_model=list[CityReadWithTemperatures])
async def get_cities(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    return await get_city_list_pagination(session=session, skip=skip, limit=limit)


@city_router.delete("/cities/{city_id}")
async def destroy_city(city_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_city_by_id(city_id=city_id, session=session)
