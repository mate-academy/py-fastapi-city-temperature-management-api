from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, crud, weather_service
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


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
            status_code=409,
            detail=f"City with name '{city.name}' already exists."
        )
    return crud.create_city(db=db, city=city)



@app.post("/temperatures/update")
async def update_all_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()

    updated_count = 0
    for city in cities:
        temp_val = await weather_service.get_current_temp(city.name)

        if temp_val is not None:
            new_record = models.Temperature(city_id=city.id, temperature=temp_val)
            db.add(new_record)
            updated_count += 1

    db.commit()
    return {"message": f"Successfully updated temperatures for {updated_count} cities."}


@app.get("/temperatures", response_model=List[schemas.Temperature])
def read_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Temperature)
    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)
    return query.all()