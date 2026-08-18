from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
import crud
import services
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cities Weather API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities",
          response_model=schemas.CityResponse,
          status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, name=city.name):
        raise HTTPException(status_code=400, detail="City already exists")
    return crud.create_city(db, city)


@app.get("/cities", response_model=List[schemas.CityResponse])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@app.get("/cities/{city_id}", response_model=schemas.CityResponse)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.CityResponse)
def update_city(city_id: int,
                city_data: schemas.CityUpdate,
                db: Session = Depends(get_db)):
    updated_city = crud.update_city(db, city_id, city_data)
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    if not crud.delete_city(db, city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return None


@app.post("/temperatures/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    updated_records = []

    for city in cities:
        try:
            temp = await services.fetch_city_temperature(city.name)
            # record = crud.create_temperature_record(db, city.id, temp)
            updated_records.append({"city": city.name, "temperature": temp})
        except Exception:
            continue

    return {"message": "City temperature update successfully",
            "data": updated_records}


@app.get("/temperatures",
         response_model=List[schemas.TemperatureResponse])
def read_temperatures(city_id: Optional[int] = None,
                      db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
