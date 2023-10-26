from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import get_temperature, get_temperatures, delete_temperature, get_city, get_cities
from db.engine import SessionLocal
from schemas import TemperatureList, CityList, CityCreate, TemperatureCreate

app = FastAPI()


# Dependency to get the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# City Endpoints
@app.post("/cities/", response_model=CityList)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db=db, city=city)


@app.get("/cities/", response_model=list[CityList])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = get_cities(db, skip=skip, limit=limit)
    return cities


@app.get("/cities/{city_id}", response_model=CityList)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.put("/cities/{city_id}", response_model=CityList)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    return update_city(db=db, city_id=city_id, city=city)


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    delete_city(db=db, city_id=city_id)
    return {"status": "successful"}


# Temperature Endpoints

@app.post("/temperatures/", response_model=TemperatureList)
def create_temperature(temperature: TemperatureCreate, db: Session = Depends(get_db)):
    return create_temperature(db=db, temperature=temperature)


@app.get("/temperatures/", response_model=list[TemperatureList])
def read_temperatures(skip: int = 0, limit: int = 100, city_id: int = None, db: Session = Depends(get_db)):
    return get_temperatures(db, skip=skip, limit=limit, city_id=city_id)


@app.get("/temperatures/{temperature_id}", response_model=TemperatureList)
def read_temperature(temperature_id: int, db: Session = Depends(get_db)):
    db_temperature = get_temperature(db, temperature_id=temperature_id)
    if db_temperature is None:
        raise HTTPException(status_code=404, detail="Temperature record not found")
    return db_temperature


@app.delete("/temperatures/{temperature_id}")
def delete_temperature(temperature_id: int, db: Session = Depends(get_db)):
    delete_temperature(db=db, temperature_id=temperature_id)
    return {"status": "successful"}
