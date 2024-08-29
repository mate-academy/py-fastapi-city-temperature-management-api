from fastapi import APIRouter, Depends
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas, crud
from app.dependencies import get_db, CommonsDep

router = APIRouter()


@router.get("/", response_model=list[schemas.City])
async def get_cities(
    commons: CommonsDep, db: AsyncSession = Depends(get_db)
) -> Sequence[schemas.City]:
    return await crud.get_all_cities(
        db=db, skip=commons["skip"], limit=commons["limit"]
    )


@router.post("/", response_model=schemas.CityCreate)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/{city_id}", response_model=schemas.City)
async def get_city_by_id(
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> schemas.City:
    return await crud.get_city_by_id(db=db, city_id=city_id)


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.update_city(db=db, city_id=city_id, city_update=city)


@router.delete("/{city_id}", status_code=204)
async def delete_city(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    await crud.delete_city(db=db, city_id=city_id)
