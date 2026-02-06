from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas, models
from city.models import DBCity
from dependencies import get_db

router = APIRouter()


@router.get(
    "/cities/",
    response_model=schemas.PaginatedResponse[schemas.City]
)
async def list_of_cities(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: int = 1,
        size: int = 10,
        city: str = None
) -> dict[str, schemas.City]:
    return await crud.get_all_cities(db, page, size, city)


@router.get("/cities/{db_city_id}/", response_model=schemas.City)
async def get_city(
        db_city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> models.DBCity:
    db_city = await crud.get_city_by_id(db, db_city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> models.DBCity:
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)
    if db_city is not None:
        raise HTTPException(status_code=400, detail="City already exists")
    return await crud.create_city(db, city)


@router.delete("/cities/{city_id}/")
async def delete_city(
        city_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    db_city = await crud.get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.delete_city_by_id(db, db_city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        update_data: schemas.CityUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> models.DBCity:
    db_city = await crud.get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.city_update(db=db, city=db_city,
                                  update_data=update_data.model_dump())


@router.patch("/cities/{city_id}/", response_model=schemas.City)
async def patch_city(
        city_id: int,
        city_patch: schemas.CityPatch,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> models.DBCity:
    db_city = await crud.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    update_data = city_patch.model_dump(exclude_unset=True)

    return await crud.city_update(db, db_city, update_data)
