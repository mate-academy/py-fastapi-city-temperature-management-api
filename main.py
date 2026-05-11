from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx

import models, schemas, database

# Створення таблиць у базі даних (якщо їх ще немає)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="City Temperature API")


# Dependency для отримання сесії БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# Part 1: City CRUD API
# ==========================================

@app.get("/")
def read_root():
    return {"message": "Welcome to the City Temperature API! Go to /docs to see the documentation."}

@app.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    try:
        db.commit()
        db.refresh(db_city)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="City already exists or invalid data")
    return db_city


@app.get("/cities", response_model=List[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city_update.name
    db_city.additional_info = city_update.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": "City deleted successfully"}


# ==========================================
# Part 2: Temperature API
# ==========================================

@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        return {"message": "No cities in database to update."}

    updated_count = 0
    # Використовуємо асинхронний клієнт HTTPX
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                # Використовуємо wttr.in як безкоштовне API без ключів
                response = await client.get(f"https://wttr.in/{city.name}?format=%t")
                if response.status_code == 200:
                    # Очищаємо рядок (наприклад, перетворюємо "+15°C" на 15.0)
                    temp_str = response.text.replace('°C', '').replace('+', '').replace('°F', '').strip()
                    temp_val = float(temp_str)

                    new_temp = models.Temperature(city_id=city.id, temperature=temp_val)
                    db.add(new_temp)
                    updated_count += 1
            except Exception as e:
                print(f"Error fetching temperature for {city.name}: {e}")

        db.commit()

    return {"message": f"Successfully updated temperatures for {updated_count} out of {len(cities)} cities."}


@app.get("/temperatures", response_model=List[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()