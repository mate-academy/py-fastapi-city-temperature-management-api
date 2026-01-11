from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.engine import SessionLocal
from . import crud, schemas


router = APIRouter(prefix="/cities", tags=["cities"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@router.get("/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted"}


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city_update: schemas.CityCreate, db: Session = Depends(get_db)
):
    city = crud.update_city(db, city_id, city_update)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
