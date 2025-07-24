from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import city as schemas
from app.crud import city as crud
from app.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cities", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)

@router.get("/cities", response_model=list[schemas.City])
def list_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)

@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
