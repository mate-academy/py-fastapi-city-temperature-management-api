from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.post_city(city_schema=city, db=db)


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def retrieve_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_detail(city_id=city_id, db=db)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_schema: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
):
    city = await crud.update_city(city_id=city_id, city_schema=city_schema, db=db)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/cities/{city_id}", response_model=dict)
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_city(city_id=city_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted successfully."}
