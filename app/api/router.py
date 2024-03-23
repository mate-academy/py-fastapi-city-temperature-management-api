from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import aiohttp

from app import crud, schemas
from app import dependencies
router = APIRouter()


@router.post('/temperatures/update')
async def update_temperature(city_id: int,
                             db: Session = Depends(dependencies.get_db)) -> schemas.Temperature:  # noqa:E501
    city = crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail='City not found')
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=bb5878760b3f454b2ceaea8ed25f5021"  # noqa:E501, E231

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                content = await response.text()
                raise HTTPException(status_code=response.status,
                                    detail=f"Error fetching weather data: {content}")  # noqa:E501
            data = await response.json()
            temperature = data['main']['temp']
            temperature_celsius = temperature - 273.15
            temperature_celsius_rounded = round(temperature_celsius, 2)
            temperature_record = schemas.TemperatureCreate(
                date_time=datetime.now(),
                temperature=temperature_celsius_rounded
            )

            return crud.create_temperature_record(db=db,
                                                  temperature=temperature_record,  # noqa:E501
                                                  city_id=city_id)

app = FastAPI()

app.include_router(router)
