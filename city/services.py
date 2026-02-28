from fastapi import HTTPException
from sqlalchemy.orm import Session

from city.models import City
from city.schemas import CityCreateUpdateDto
from city.crud import (
    db_read_cities,
    db_create_city,
    db_read_city,
    db_delete_city,
    db_update_city
)


def service_read_cities(
    db: Session
) -> list[City]:
    return db_read_cities(db=db)


def service_create_city(
    city: CityCreateUpdateDto,
    db: Session
) -> City:
    try:
        created_city = db_create_city(
            City(
                name=city.name,
                additional_info=city.additional_info
            ),
            db=db
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Name must be at least 3 characters"
        )
    if created_city is None:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists"
        )
    return created_city 


def service_read_city(
    id: int,
    db: Session
) -> City:
    city = db_read_city(
        id=id,
        db=db
    )
    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return city 


def service_update_city(
    id: int,
    city: CityCreateUpdateDto,
    db: Session
) -> City:
    try:
        updated_city = db_update_city(
            id=id,
            city=City(
                name=city.name,
                additional_info=city.additional_info
            ),
            db=db
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Name must be at least 3 characters"
        )
    if not updated_city:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return updated_city


def service_delete_city(
    id: int,
    db: Session
) -> dict:
    result = db_delete_city(
        id=id,
        db=db
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return {
        "message": "City deleted successfully"
    }
