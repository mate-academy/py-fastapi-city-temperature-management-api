from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud
from .models import City

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> list[City]:
    return crud.get_all_cities(db=db, skip=skip, limit=limit)


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
) -> City:
    db_city = crud.get_city_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for City already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> City | None:
    db_city = crud.get_single_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
        city_id: int,
        name: str,
        additional_info: str,
        db: Session = Depends(get_db)
) -> City:
    db_city = crud.update_city(
        db=db,
        city_id=city_id,
        name=name,
        additional_info=additional_info
    )

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> dict:
    db_city = crud.delete_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city
