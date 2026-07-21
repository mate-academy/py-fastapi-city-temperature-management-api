from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.city import crud, schemas, models
from app.dependencies import get_db

router = APIRouter()


@router.get("/cities", response_model=list[schemas.CityModel])
async def get_all_cities(db: AsyncSession = Depends(get_db)) -> list[models.City]:
    return await crud.get_city_list(db)


@router.get("/cities/{city_id}", response_model=schemas.CityModel)
async def get_single_city(
    city_id: int,
    db: AsyncSession = Depends(get_db)
) -> models.City:
    city = await crud.get_city_by_id(db, city_id)

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return city
