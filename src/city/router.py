from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.city import schemas, service

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
)


@router.get("/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return service.get_all_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = service.get_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    return service.create_city(db=db, city=city)


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    return service.update_city(db=db, city_id=city_id, city=city)


@router.delete("/{city_id}")
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    return service.delete_city(db=db, city_id=city_id)
