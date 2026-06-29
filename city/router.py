import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import schemas, crud
from city.utils import get_weather
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def list_of_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/cities/", response_model=schemas.CityCreate)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.CityUpdate)
def update_city(
        city: schemas.CityUpdate,
        city_id: int,
        db: Session = Depends(get_db)
):
    db_city = crud.update_city(db=db, city_id=city_id, city=city)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.delete_city(db=db, city_id=city_id)


@router.get("/temperature/", response_model=list[schemas.Temperature])
def get_temperature_list(
        city_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_all_temperature(db=db, city_id=city_id)


@router.post("/temperature/update/")
async def update_all_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_all_cities(db=db)
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(get_weather(city.name))
            for city in cities
        ]

    for city, task in zip(cities, tasks):
        temperature = task.result()
        if temperature is None:
            continue
        crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=temperature
        )
