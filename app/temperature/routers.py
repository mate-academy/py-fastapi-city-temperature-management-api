from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.temperature import crud, schemas
from app.depencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Temperature)
def create_temperature(
        temperature: schemas.TemperatureCreate, db: Session = Depends(get_db)
):
    return crud.create_temperature(db=db, temperature=temperature)


@router.get("/", response_model=list[schemas.Temperature])
def get_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db=db)


@router.get("/{city_id}", response_model=list[schemas.Temperature])
def get_temperature_by_city(city_id: int, db: Session = Depends(get_db)):
    temperatures = crud.get_temperatures_by_city(
        db=db,
        city_id=city_id
    )
    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperatures found for this city"
        )
    return temperatures
