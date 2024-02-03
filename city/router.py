from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud, models
from dependencies import get_db, CommonsDep

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
    commons: CommonsDep, db: AsyncSession = Depends(get_db)
) -> list[models.CityDB]:
    query = await crud.get_all_cities(db=db, commons=commons)
    return query


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
) -> dict[str | None]:
    created_city = await crud.create_city(db=db, city=city)
    return created_city


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city_by_id(
    city_id: int, db: AsyncSession = Depends(get_db)
) -> models.CityDB:
    result = await crud.get_city_by_id(db=db, city_id=city_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int, updated_city: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
):
    result = await crud.update_city(db=db, city_id=city_id, updated_city=updated_city)
    return result


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_city(db=db, city_id=city_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="City not found")
