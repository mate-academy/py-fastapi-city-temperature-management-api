from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
        "/",
        response_model=schemas.City,
        status_code=status.HTTP_201_CREATED
)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
):
    if await crud.get_city_by_name(db, city.name):
        raise HTTPException(status_code=400, detail="City already exists")
    return await crud.create_city(db, city)


@router.get("/", response_model=list[schemas.City])
async def list_cities(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, data: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    existing = await crud.get_city_by_name(db, data.name)
    if existing and existing.id != city_id:
        raise HTTPException(status_code=400, detail="City name already in use")
    return await crud.update_city(db, city, data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db, city)
