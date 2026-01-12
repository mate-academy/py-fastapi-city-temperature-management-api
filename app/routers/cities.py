from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import CityCreate, CityUpdate, City

from fastapi import Depends, HTTPException, APIRouter


router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/cities/", response_model=list[City])
def read_city(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return crud.get_all_cities(db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    city_db = crud.get_city(db=db, city_id=city_id)
    if not city_db:
        raise HTTPException(status_code=404, detail="City not found")
    return city_db


@router.post("/cities/", response_model=City)
def create_author(city: CityCreate, db: Session = Depends(get_db)):

    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=City)
def update_city(city_id: int, city_data: CityUpdate, db: Session = Depends(get_db)):

    updated_city = crud.update_city(db=db, city_id=city_id, city_data=city_data)

    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete("/cities/{city_id}/", response_model=City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = crud.delete_city(db=db, city_id=city_id)
    if not deleted_city:
        raise HTTPException(status_code=404, detail="City not found")
    return deleted_city
