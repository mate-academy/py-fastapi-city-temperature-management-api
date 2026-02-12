import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
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
    cities = city_crud.get_all_cities(db)
    temperatures = await asyncio.gather(*(fetch_temperature(city.name) for city in cities))

    for city, temperature in zip(cities, temperatures):
        if temperature is not None:
            temp_crud.create_temperature(db, city.id, temperature)

    return {"message": "Temperatures updated successfully"}


@router.get("", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    temperatures = crud.get_temperatures(db=db, city_id=city_id)

    if city_id is not None and not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperature records found for this city"
        )

    return temperatures
