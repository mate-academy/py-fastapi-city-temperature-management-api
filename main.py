from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, crud, weather_service
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="City Temperature Management System")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/cities", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    existing_city = crud.get_city_by_name(db, name=city.name)
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city.name}' already exists."
        )
    return crud.create_city(db=db, city=city)


@app.get("/cities", response_model=List[schemas.City])
def read_all_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    success = crud.delete_city(db, city_id=city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return None



@app.post("/temperatures/update")
async def update_all_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    if not cities:
        return {"message": "No cities found to update."}

    updated_count = 0
    for city in cities:
        temp_val = await weather_service.get_current_temp(city.name)

        if temp_val is not None:
            crud.create_temperature(db, city_id=city.id, temperature=temp_val)
            updated_count += 1

    return {"message": f"Successfully updated temperatures for {updated_count} cities."}


@app.get("/temperatures", response_model=List[schemas.Temperature])
def read_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)