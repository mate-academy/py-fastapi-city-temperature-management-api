import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy.orm import Session

from city import crud as city_crud
from dependencies import get_db
from settings import settings
from temperature import schemas, crud, models

router = APIRouter()

load_dotenv()

API_KEY = os.environ["WEATHER_API_KEY"]


async def get_weather(city: str, client: AsyncClient()) -> tuple:
    response = await client.get(
        settings.WEATHER_API_URL, params={"key": API_KEY, "q": city}
    )
    data = response.json()
    return data["location"]["name"], data["current"]["temp_c"]


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def list_temperatures(
    city_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    queryset = db.query(models.Temperature)
    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)

    return queryset.offset(skip).limit(limit).all()


@router.post("/temperatures/update", response_model=dict)
async def update_temperatures(db: Session = Depends(get_db)):
    try:
        cities = city_crud.get_all_cities(db=db)
        dict_cities = {city.name: city.id for city in cities}

        async with AsyncClient() as client:
            cities_temp = await asyncio.gather(
                *[get_weather(city, client) for city in dict_cities.keys()]
            )
        for city in cities_temp:
            db_temp = crud.get_temperature_by_city_id(
                db=db, city_id=dict_cities[city[0]]
            )
            if db_temp is None:
                crud.create_temperature(
                    db=db, city_id=dict_cities[city[0]], temp=city[1]
                )
            else:
                crud.update_temperature(
                    db=db, city_id=dict_cities[city[0]], temp=city[1]
                )

        return {"message": "Temperatures updated successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
