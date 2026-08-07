from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from main import app, get_db


@app.get("/cities/", response_model=list[schemas.City])
def read_cities(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return crud.get_all_cities(db, skip=skip, limit=limit)

@app.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_name(db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return crud.create_city(db, city=city)

@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):

    city = crud.get_city_by_id(db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=400,
            detail="City with this id does not exist"
        )
    return city

@app.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_id(db, city_id)

    if db_city is None:
        raise HTTPException(
            status_code=400,
            detail="City with this id does not exist"
        )

    return crud.update_city(db, city_id, city)

@app.delete("/cities/{city_id}")
def delete_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    city = crud.get_city_by_id(db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=400,
            detail="City with this id does not exist"
        )
    return crud.delete_city(db, city_id=city_id)
