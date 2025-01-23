from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from city_temp.city.crud import (
    create_city as create_city_crud,
    get_cities,
    get_city_by_id,
    update_city as update_city_crud,
    delete_city as delete_city_crud,
)
from city_temp.city.schemas import CityCreate, City
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return create_city_crud(db=db, city=city)


@router.get("/cities/", response_model=list[City])
def list_cities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=City)
def city_detail(city_id: int, db: Session = Depends(get_db)):
    db_city = get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}/", response_model=City)
def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = update_city_crud(db=db, city_id=city_id, city=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}/", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = delete_city_crud(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
