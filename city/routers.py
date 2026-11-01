from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import schemas, crud
from models.city import DBCity
from database import get_db

city_router = APIRouter()


#---------------------------city-----------------
# Read (GET)
@city_router.get("/cities/", response_model=list[schemas.CityRead])
def read_cities(
    db: Session = Depends(get_db),
) -> list[DBCity]:
    return crud.get_all_cities(db)


# Read (GET)
@city_router.get("/cities/{city_id}", response_model=schemas.CityRead)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="No such city!")
    else:
        return db_city


# CREATE (POST)
@city_router.post("/cities/", response_model=schemas.CityRead)
def create_cities(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    return crud.create_city(db=db, city=city)


# Delete (DELETE)
@city_router.delete("/cities/{city_id}")
def delete_item(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db, city_id)
