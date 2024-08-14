from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from city import crud, schemas
from dependencies import get_db
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post("/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="City already registered"
        )
    return await crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
async def read_cities(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
) -> List[schemas.City]:
    cities = await crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/{city_id}", response_model=schemas.City)
async def read_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    await db.commit()
    await db.refresh(db_city)

    return db_city


@router.delete("/{city_id}", response_class=JSONResponse)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    db_city = await crud.get_city_by_id(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    await crud.delete_city(db=db, city_id=city_id)
    return JSONResponse(
        status_code=200,
        content={"message": "The city was successfully deleted"}
    )
