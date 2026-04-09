from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from city.schemas import City, CityCreate
from city import crud, models
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(city=city, db=db)


@router.get("/cities/", response_model=list[City])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/cities/{city_id}/", response_model=City)
def get_specific_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).get(city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.get_city(city_id=city_id, db=db)


@router.put("/cities/{city_id}/", response_model=City)
def update_city(
    city_id: int,
    city: CityCreate,
    db: Session = Depends(get_db)
):
    return crud.update_city_by_id(city_id=city_id, city=city, db=db)


@router.delete("/cities/{city_id}/", response_model=City)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_city_by_id(city_id=city_id, db=db)
