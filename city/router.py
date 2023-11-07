from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


from dependencies import get_db
from city import crud
from city.schemas import City, CityCreate

router = APIRouter()


@router.get("/city/", response_model=list[City])
async def read_city(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_city(db=db)


@router.post("/city", response_model=City)
async def create_city(
    city: CityCreate,
    db: AsyncSession = Depends(get_db)
):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name for City already exists"
        )
    return await crud.create_city(db=db, city=city)


@router.get("/city/{city_id}/", response_model=City)
async def read_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return await db_city


@router.delete("/city/{city_id}/", response_model=City)
async def delete_single_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(db_city)
    await db.commit()
    return db_city


@router.put("/city/{city_id}/", response_model=City)
async def update_single_city(
        city_id: int, city: CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    for attr, value in city.model_dump().items():
        if attr is not None:
            setattr(db_city, attr, value)
    await db.commit()
    await db.refresh(db_city)
    return db_city
