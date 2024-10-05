from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.city import crud, schemas
from app.dependencies import get_db

city_router = APIRouter()


@city_router.post("/", response_model=schemas.CityRead)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@city_router.get("/", response_model=list[schemas.CityRead])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@city_router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"ok": True}
