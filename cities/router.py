from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from cities import crud
from dependencies import DbSession
from models import City as CityModel
from schemas.city import City, CityCreate, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


def get_city_or_404(city_id: int, db: DbSession) -> CityModel:
    city = crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found",
        )
    return city


ExistingCity = Annotated[CityModel, Depends(get_city_or_404)]


def ensure_name_is_free(db: DbSession, name: str) -> None:
    if crud.get_city_by_name(db=db, name=name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City '{name}' already exists",
        )


@router.post("/", response_model=City, status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: DbSession):
    ensure_name_is_free(db=db, name=city.name)
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[City])
def list_cities(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=City)
def get_city(city: ExistingCity):
    return city


@router.put("/{city_id}", response_model=City)
def update_city(city_data: CityUpdate, city: ExistingCity, db: DbSession):
    if city_data.name and city_data.name != city.name:
        ensure_name_is_free(db=db, name=city_data.name)
    return crud.update_city(db=db, db_city=city, city=city_data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city: ExistingCity, db: DbSession):
    crud.delete_city(db=db, db_city=city)
