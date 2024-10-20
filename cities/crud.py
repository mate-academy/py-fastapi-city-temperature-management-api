from typing import List

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from dependencies import ListDep, CityItemDep
from cities.models import DbCity
from cities.schemas import CityBase, CityCreate, City


def get_all_cities(commons: ListDep) -> List[City]:
    db = commons["db"]
    q = commons["q"]
    skip = commons["skip"]
    limit = commons["limit"]

    query = db.query(DbCity)

    if q:
        query = query.filter(DbCity.name.contains(q))

    cities = query.offset(skip).limit(limit).all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found matching the query."
        )

    return cities


def get_city(commons: CityItemDep) -> City:
    db, city_id = commons

    city = db.query(DbCity).filter(DbCity.id == city_id).first()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id {city_id} not found"
        )

    return city


def update_city(commons: CityItemDep, city_update: CityBase) -> City:
    db, city_id = commons

    city = get_city(commons)

    city.name = city_update.name
    city.additional_info = city_update.additional_info

    db.commit()
    db.refresh(city)

    return city


def create_city(db: Session, city: CityCreate) -> City:
    city = DbCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(city)
    db.commit()
    db.refresh(city)

    return city


def delete_city(commons: CityItemDep) -> dict[str, str]:
    db, city_id = commons

    city = get_city(commons)

    db.delete(city)
    db.commit()

    return {"detail": f"City with id {city_id} has been deleted successfully"}
