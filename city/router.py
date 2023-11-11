from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city import crud, models, schemas
from database import engine
from dependencies import get_db
from pretty_response import PrettyJSONResponse

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.CityCreateUpdate,
    response_class=PrettyJSONResponse,
)
def create_city(city: schemas.CityCreateUpdate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.get(
    "/",
    response_model=list[schemas.CityRead],
    response_class=PrettyJSONResponse,
)
def read_cities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities


@router.get(
    "/{city_id}",
    response_model=schemas.CityRead,
    response_class=PrettyJSONResponse,
)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db=db, city_id=city_id)
    return city


@router.put(
    "/{city_id}",
    response_model=schemas.CityRead,
    response_class=PrettyJSONResponse,
)
def update_city(
    city_id: int, city: schemas.CityCreateUpdate, db: Session = Depends(get_db)
):
    city = crud.update_city(db=db, city_id=city_id, city=city)
    return city


@router.delete("/{city_id}", response_class=PrettyJSONResponse)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    result = crud.delete_city(db=db, city_id=city_id)
    if result is True:
        return {"message": "City deleted"}
    else:
        return {"message": "City not found"}
