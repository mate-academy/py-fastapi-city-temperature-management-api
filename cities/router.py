from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from cities import crud
from cities.schemas import City, CreateCity, UpdateCity
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/cities/", response_model=list[City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_city_list(db=db)


@router.get("/cities/{city_id}/", response_model=City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city(db=db, city_id=city_id)


@router.post("/cities/", response_model=City)
def create_city(city: CreateCity, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=City)
def update_cities(city_id: int, city: UpdateCity, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/")
def delete_cities(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)
