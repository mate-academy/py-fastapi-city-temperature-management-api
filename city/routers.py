from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from city.schemas import CityDto, CityCreateUpdateDto
from city.services import (
    service_read_cities,
    service_create_city,
    service_read_city,
    service_delete_city,
    service_update_city
)


city_router = APIRouter(
    prefix="/cities",
    tags=["cities"]
)


@city_router.get("/", response_model=list[CityDto])
def get_cities(
    db: Session = Depends(get_db)
):
    return service_read_cities(db=db)


@city_router.post("/", response_model=CityDto)
def post_city(
    city: CityCreateUpdateDto,
    db: Session = Depends(get_db)
):
    return service_create_city(
        city=city,
        db=db
    )


@city_router.get("/{id}/", response_model=CityDto)
def get_city(
    id: int,
    db: Session = Depends(get_db)
):
    return service_read_city(
        id=id,
        db=db
    )


@city_router.put("/{id}/", response_model=CityDto)
def update_city(
    id: int,
    city: CityCreateUpdateDto,
    db: Session = Depends(get_db)
):
    return service_update_city(
        id=id,
        city=city,
        db=db
    )


@city_router.delete("/{id}/", response_model=dict)
def delete_city(
    id: int,
    db: Session = Depends(get_db)
):
    return service_delete_city(
        id=id,
        db=db
    )
