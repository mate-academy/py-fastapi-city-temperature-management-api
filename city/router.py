from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, pagination_parameters
from . import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityRead])
async def read_cities(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(pagination_parameters),
):
    try:
        cities = await crud.get_all_cities(
            db=db, skip=pagination["skip"], limit=pagination["limit"]
        )
        return cities
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при отриманні міст")


@router.post("/cities/", response_model=schemas.CityRead)
async def create_city(new_city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    try:
        city = await crud.create_city(db=db, city=new_city)
        return city
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при створенні міста")


@router.get("/cities/{city_id}", response_model=schemas.CityRead)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        city = await crud.get_city(db=db, city_id=city_id)
        if city is None:
            raise HTTPException(status_code=404, detail="Місто не знайдено")
        return city
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при отриманні міста")


@router.put("/cities/{city_id}", response_model=schemas.CityRead)
async def update_city(
    city_id: int, city_updates: schemas.CityUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        db_city = await crud.get_city(db=db, city_id=city_id)
        if db_city is None:
            raise HTTPException(status_code=404, detail="Місто не знайдено")
        updated_city = await crud.update_city(
            db=db, db_city=db_city, city_updates=city_updates
        )
        return updated_city
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при оновленні міста")


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    try:
        city_to_delete = await crud.get_city(db=db, city_id=city_id)
        if city_to_delete is None:
            raise HTTPException(status_code=404, detail="Місто не знайдено")
        await crud.delete_city(db=db, city_to_delete=city_to_delete)
        return {"detail": "Місто успішно видалено"}
    except HTTPException as he:
        raise he
    except Exception:
        raise HTTPException(status_code=500, detail="Помилка при видаленні міста")
