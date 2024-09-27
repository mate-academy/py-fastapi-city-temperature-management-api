import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, schemas
from temperature.utils import fetch_city_temperature
from city.models import City

from dependencies import get_db


router = APIRouter(tags=["Temperature Operations"])


@router.post("/temperatures/update/", response_model=List[schemas.Tempereture])
async def update_temperatures(
    db: Session = Depends(get_db)
) -> List[schemas.Tempereture]:
    cities = db.query(City).all()
    tasks = []

    for city in cities:
        tasks.append(fetch_city_temperature(city.name))

    results = await asyncio.gather(*tasks)

    updated_temperatures = []
    for city, temp in zip(cities, results):
        if temp is not None:
            new_temperature = crud.create_temperature(
                db=db,
                temperature=schemas.TemperetureCreate(
                    city_id=city.id,
                    temperature=temp,
                )
            )
            updated_temperatures.append(new_temperature)

    return updated_temperatures


@router.get("/temperatures/", response_model=List[schemas.Tempereture])
def read_temperatures(
    skip: int = 0,
    limit: int = 10,
    city_id: int = Query(None),
    db: Session = Depends(get_db)
) -> Optional[List[schemas.Tempereture]]:
    if city_id:
        temperatures = crud.get_temperatures_by_city(
            db,
            city_id,
            skip=skip,
            limit=limit
        )
        if not temperatures:
            raise HTTPException(status_code=404, detail="City not found")
        return temperatures

    return crud.get_all_temperatures(db=db, skip=skip, limit=limit)
