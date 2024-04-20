import httpx
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
import asyncio
from dependencies import get_db
from temperature import schemas
from city.crud import get_all_cities
from temperature.temp_parser import get_temperatures
from temperature import crud
from temperature import models

router = APIRouter()


@router.get("/temperatures/{city_id}", response_model=List[schemas.Temperature])
def get_temperature_for_specific_city(
        city_id: int | None = None,
        db: Session = Depends(get_db),
) -> List[schemas.Temperature]:

    temperatures = crud.get_temperature_for_specific_city(db=db, city_id=city_id)

    return temperatures


@router.get("/temperatures/", response_model=List[schemas.Temperature])
def read_temperatures(
        skip: int = Query(0),
        limit: int = Query(10),
        db: Session = Depends(get_db)
) -> List[schemas.Temperature]:

    temperatures = crud.get_all_temperatures_with_pagination(
        db=db, skip=skip, limit=limit
    )

    return temperatures


@router.get("/temperatures/update/", response_model=List[schemas.Temperature])
async def update_temperatures_for_all_cities(
        db: Session = Depends(get_db)
) -> List[schemas.Temperature]:
    all_cities = get_all_cities(db=db)

    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            temp_results = [
                {
                    "temperature": tg.create_task(
                        get_temperatures(city_name=city.name, client=client)
                    ),
                    "city_id": city.id,
                }
                for city in all_cities
            ]

    temperatures = [
        crud.create_temperature(
            db=db,
            temp=result["temperature"].result(),
            city_id=result["city_id"],
        )
        for result in temp_results
    ]

    return temperatures
