from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.city import crud, schemas, models
from app.dependencies import get_db

router = APIRouter()


@router.get("/cities", response_model=list[schemas.CityModel])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> list[models.City]:
    return await crud.get_city_list(db)
