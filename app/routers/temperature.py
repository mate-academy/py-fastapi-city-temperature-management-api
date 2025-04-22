from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
)


@router.post("/{city_id}", response_model=schemas.Temperature)
def create_temperature(
    city_id: int,
    temperature: schemas.TemperatureCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_temperature(db=db, temperature=temperature, city_id=city_id)


@router.get("/", response_model=List[schemas.Temperature])
def get_temperatures(
    skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)
):
    return crud.get_temperatures(db=db, skip=skip, limit=limit)


@router.get("/{temperature_id}", response_model=schemas.Temperature)
def get_temperature(temperature_id: int, db: Session = Depends(database.get_db)):
    db_temperature = crud.get_temperature(db=db, temperature_id=temperature_id)
    if not db_temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return db_temperature


@router.put("/{temperature_id}", response_model=schemas.Temperature)
def update_temperature(
    temperature_id: int,
    temperature: schemas.TemperatureCreate,
    db: Session = Depends(database.get_db),
):
    db_temperature = crud.update_temperature(
        db=db, temperature_id=temperature_id, temperature=temperature
    )
    if not db_temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return db_temperature


@router.delete("/{temperature_id}", response_model=schemas.Temperature)
def delete_temperature(
    temperature_id: int, db: Session = Depends(database.get_db)
):
    db_temperature = crud.delete_temperature(db=db, temperature_id=temperature_id)
    if not db_temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return db_temperature
