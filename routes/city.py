from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.dependencies import get_db
from schemas.city import CityResponse, CreateCityRequest
import crud.city as crud


router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", status_code=201, response_model=CityResponse)
async def create_city(
    city_request: CreateCityRequest, db: AsyncSession = Depends(get_db)
):
    result = await crud.create_city(db=db, city_request=city_request)
    if result is None:
        raise HTTPException(
            status_code=404, detail="City with this name already exists."
        )
    return result


@router.get("/", status_code=200, response_model=list[CityResponse])
async def get_cities(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_cities(db)
    return cities


@router.get("/{id}", response_model=CityResponse)
async def get_city(id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(id, db)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.put("/{id}", status_code=200, response_model=CityResponse)
async def update_city(
    id: int, city_request: CreateCityRequest, db: AsyncSession = Depends(get_db)
):
    result = await crud.update_city(db=db, city_id=id, city_request=city_request)
    if result is None:
        raise HTTPException(
            status_code=400, detail="City with this name already exists."
        )
    return result


@router.delete("/{id}", status_code=204)
async def delete_city(id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_city(db=db, city_id=id)
    city = result.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found.")

    await db.delete(city)
    await db.commit()

    return None
