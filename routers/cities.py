from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud
from crud import get_city_by_id
from database import get_db
from models import City
from schema import CityRead, CityCreate


router = APIRouter()

@router.get("/", response_model=list[CityRead])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db)


@router.post("/", response_model=CityRead, status_code=201)
def create_city(
        city_data: CityCreate,
        db: Session = Depends(get_db),
):
    return crud.create_city(db, city_data)


@router.delete("/{city_id}", response_model=CityRead)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = get_city_by_id(city_id, db)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    return city