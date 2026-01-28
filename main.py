from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.base import Base
from db.session import engine
from db.deps import get_db

from models.city import City

from schemas.city import CityCreate, CityRead
from schemas.temperature import TemperatureRead

from crud.city import create_city, get_cities, get_city, delete_city
from crud.temperature import create_temperature, get_temperatures

from services.weather import fetch_temperature

Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management API")


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/cities", response_model=CityRead, status_code=status.HTTP_201_CREATED)
def create_city_api(
    city: CityCreate,
    db: Session = Depends(get_db)
):
    return create_city(db, city)


@app.get("/cities", response_model=list[CityRead])
def get_cities_api(db: Session = Depends(get_db)):
    return get_cities(db)


@app.get("/cities/{city_id}", response_model=CityRead)
def get_city_api(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city_api(
    city_id: int,
    db: Session = Depends(get_db)
):
    city = get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    delete_city(db, city)


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).all()

    for city in cities:
        temperature = await fetch_temperature(city.name)
        create_temperature(db, city.id, temperature)

    return {
        "status": "ok",
        "cities_updated": len(cities)
    }


@app.get("/temperatures", response_model=list[TemperatureRead])
def read_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_temperatures(db, city_id)
