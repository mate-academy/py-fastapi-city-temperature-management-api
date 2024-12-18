from fastapi import FastAPI, Depends, HTTPException
from database import engine, Base, get_db
import crud
from schemas import CityCreate, TemperatureCreate
from sqlalchemy.orm import Session

# Ініціалізація бази даних
Base.metadata.create_all(bind=engine)

# Ініціалізація FastAPI
app = FastAPI()


# Ендпоінти для Cities
@app.get("/cities/")
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@app.post("/cities/")
def add_city(city: CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@app.put("/cities/{city_id}/")
def update_city(
        city_id: int, updated_data: CityCreate, db: Session = Depends(get_db)
):
    updated_city = crud.update_city(db, city_id, updated_data)
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@app.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = crud.delete_city(db, city_id)
    if deleted_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}


# Ендпоінти для Temperatures
@app.get("/temperatures/")
def read_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures(db)


@app.post("/temperatures/")
def add_temperature(
        temperature: TemperatureCreate, db: Session = Depends(get_db)
):
    return crud.create_temperature(db, temperature)


# Ендпоінт для оновлення температури (POST /temperatures/update)
@app.post("/temperatures/update/")
def update_temperature(
        city_id: int, temperature_value: float, db: Session = Depends(get_db)
):
    # Можна додати інтелектуальне отримання температури через сторонній API.
    updated_temperature = crud.update_temperature(
        db, city_id, temperature_value
    )
    if updated_temperature is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_temperature
