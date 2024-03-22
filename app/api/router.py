from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import aiohttp

from app import crud, database, schemas

router = APIRouter()


@router.post('/temperatures/update')
async def update_temperature(city_id: int,
                             db: Session = Depends(database.
                                                   get_db)) -> schemas.Temperature:  # noqa:E501
    city = crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail='City not found')

    api_url = (f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=bb5878760b3f454b2ceaea8ed25f5021")  # noqa:E501

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()
            temperature = data['main']['temp']
            temperature_celsius = temperature - 273.15
            temperature_record = schemas.TemperatureCreate(
                date_time=datetime.now(),
                temperature=temperature_celsius
            )

            return crud.create_temperature_record(db=db,
                                                  temperature=temperature_record,  # noqa:E501
                                                  city_id=city_id)
