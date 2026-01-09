from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud
import httpx
from httpx import RequestError, HTTPStatusError

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City and Temperature API")


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- City Endpoints ---
@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.create_city(db, city)
    if db_city is None:
        raise HTTPException(status_code=409, detail="City already exists")
    return db_city


@app.get("/cities/", response_model=list[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    updated_city = crud.update_city(db, city_id, city)
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    success = crud.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}


# --- Temperature Endpoints ---
@app.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)


@app.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database")

    async with httpx.AsyncClient() as client:
        for city in cities:
            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={city.latitude}&longitude={city.longitude}&current_weather=true"
            )
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                temperature = data.get("current_weather", {}).get("temperature", 20.0)
                crud.create_temperature(db, city_id=city.id, temperature=temperature)
            except (RequestError, HTTPStatusError) as e:
                print(f"Failed to fetch temperature for {city.name}: {e}")
                continue

    return {"message": "Temperatures updated successfully"}
