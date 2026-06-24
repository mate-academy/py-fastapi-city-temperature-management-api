import os
import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import models
import schemas
import crud
from database import engine, get_db

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@app.get("/cities/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    if not crud.delete_city(db=db, city_id=city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted successfully"}


@app.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id)


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not configured")

    cities = crud.get_cities(db, skip=0, limit=100)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities in database")

    async with httpx.AsyncClient() as client:
        for city in cities:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"q={city.name}&appid={API_KEY}&units=metric"
            )
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                crud.create_temperature(db=db, city_id=city.id,
                                        temp_value=temp)

    return {"message": "Temperatures updated successfully"}
