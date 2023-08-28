from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import dependecies
from cities import schemas
from cities import crud

router = APIRouter()


@router.get("/", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(dependecies.get_db)):
    return await crud.get_cities_list(db=db)


@router.get("/{city_id}/", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(dependecies.get_db)):
    db_city = await crud.get_city(db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City does not exist")
    return db_city


@router.post("/", response_model=schemas.City)
async def create_city(
        city: schemas.CreateCity,
        db: AsyncSession = Depends(dependecies.get_db)
):
    city_name = city.name
    city = await crud.create_city(db=db, city=city)
    if city:
        return city
    raise HTTPException(status_code=309, detail=f"{city_name} already exists")


@router.put("/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        new_city_data: schemas.CityBase,
        db: AsyncSession = Depends(dependecies.get_db)
) -> schemas.City | HTTPException:
    city = await crud.update_city(db=db, new_city_data=new_city_data, city_id=city_id)
    if not city:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} does not exists"
        )
    return city


@router.delete("/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(dependecies.get_db)):
    success = await crud.delete_city(city_id=city_id, db=db)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} does not exists"
        )
    return {"message": f"City with id {city_id} is deleted"}
