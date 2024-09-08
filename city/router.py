from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from city import crud, schemas, models
from dependencies import get_db, pagination_params

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityListSchema])
async def get_cities_list(
        pagination: dict = Depends(pagination_params),
        db: AsyncSession = Depends(get_db)
) -> Sequence[models.City]:
    return await crud.get_cities_list(
        db=db, skip=pagination["skip"], limit=pagination["limit"]
    )


@router.post("/cities/", response_model=schemas.CitySchema)
async def create_city(
        city: schemas.CityCreateSchema, db: AsyncSession = Depends(get_db)
) -> models.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.CitySchema)
async def get_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> models.City:
    return await crud.get_city(city_id=city_id, db=db)


@router.put("/cities/{city_id}", response_model=schemas.CitySchema)
async def update_city(
        city_id: int,
        city: schemas.CityUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.update_city(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}", response_model=schemas.CitySchema)
async def delete_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> Response:
    await crud.delete_city_from_db(db=db, city_id=city_id)
    return Response(status_code=204)
