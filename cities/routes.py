from typing import List

from fastapi import Depends, HTTPException

from cities import crud
from cities.schemas import City, CityCreate, CityBase
from dependencies import ListDep, CityItemDep, get_db
from main import app
from sqlalchemy.orm import Session


@app.get("/cities/", response_model=list[City])
def read_cities(commons: ListDep) -> List[City]:
    return crud.get_all_cities(commons)


@app.get("/cities/{city_id}/", response_model=City)
def read_single_city(commons: CityItemDep) -> City:
    db_city = crud.get_city(commons)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City was not found")

    return db_city


@app.post("/cities/", response_model=City)
def create_city(city: CityCreate, db: Session = Depends(get_db)) -> City:
    return crud.create_city(db=db, city=city)


@app.put("/cities/{city_id}", response_model=City)
def update_city(commons: CityItemDep, city: CityBase) -> City:
    return crud.update_city(commons, city_update=city)


@app.delete("/cities/{city_id}", response_model=City)
def delete_city(commons: CityItemDep) -> str:
    return crud.delete_city(commons)
