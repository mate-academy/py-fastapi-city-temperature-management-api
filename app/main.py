from fastapi import Depends, HTTPException, FastAPI
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
import aiohttp

from app import crud, models, schemas, database
from app.api import router


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(router)


# Dependency
def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/cities/', response_model=schemas.City)
def create_city(city: schemas.CityCreate,
                db: Session = Depends(get_db)) -> schemas.City:
    return crud.create_city(db=db, city=city)


@app.get('/cities/', response_model=List[schemas.City])
def read_cities(skip: int = 0,
                limit: int = 100,
                db: Session = Depends(get_db)) -> List[schemas.City]:
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@app.get('/cities/{city_id}', response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)) -> schemas.City:
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail='City not found')
    return db_city


@app.delete('/cities/{city_id}', response_model=schemas.City)
def delete_city(city_id: int,
                db: Session = Depends(get_db)) -> dict:
    deleted = crud.delete_city(db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='City not found')
    return {'detail': 'City deleted'}


@router.post('/temperatures/update')
async def update_temperature(city_id: int,
                             db: Session = Depends(database.
                                                   get_db)) -> schemas.Temperature:  # noqa:E501
    city = crud.get_city(db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail='City not found')

    api_url = (f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=bb5878760b3f454b2ceaea8ed25f5021")  # noqa:E501

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
