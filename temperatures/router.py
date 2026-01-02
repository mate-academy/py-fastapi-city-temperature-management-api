import asyncio

from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from dependencies import get_db
import cities.crud as city_crud
import temperatures.crud as temp_crud
from .services import fetch_temperature
from . import crud, schemas

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.post("/update", status_code=201)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = await run_in_threadpool(city_crud.get_all_cities, db)

    async def update_city_temperature(city):
        temp = await fetch_temperature(city.name)
        if temp is not None:
            await run_in_threadpool(
                temp_crud.create_temperature,
                db,
                city.id,
                temp
            )

    await asyncio.gather(*(update_city_temperature(city) for city in cities))

    return {"message": "Temperatures updated successfully"}


@router.get("", response_model=list[schemas.Temperature])
def read_all_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db)


@router.get("/city/{city_id}", response_model=list[schemas.Temperature])
def read_city_temperatures(
    city_id: int,
    db: Session = Depends(get_db)
):
    temperatures = crud.get_temperatures(db=db, city_id=city_id)

    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperature records found for this city"
        )

    return temperatures
