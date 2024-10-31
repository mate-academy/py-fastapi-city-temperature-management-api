from dependencies import get_db
from fastapi import APIRouter, Depends, Response, status, HTTPException
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud

router = APIRouter(prefix=f"{settings.API_PREFIX}/cities")


@router.get("/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.post(
    "/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED
)
async def new_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.get("/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.retrieve_city(db=db, id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    updated_city = await crud.update_city(
        db=db,
        id=city_id,
        city_data=city.dict()
    )
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete(
    "/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.retrieve_city(db=db, id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db=db, id=city_id)
