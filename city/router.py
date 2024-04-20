from typing import List

from city.services import city_update_validation
from dependencies import get_db
from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from city import crud, models, schemas

from db.engine import SessionLocal


router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
def read_cities(
        skip: int = Query(0),
        limit: int = Query(10),
        db: Session = Depends(get_db),
) -> List[models.City]:

    cities = crud.get_all_cities_with_pagination(db=db, skip=skip, limit=limit)

    return cities


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> models.City:

    return crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
):

    city = crud.get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    deleted_city = crud.delete_city(db=db, city_id=city_id)

    return deleted_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
        city_id: int,
        new_city_name: str | None = None,
        new_additional_info: str | None = None,
        db: Session = Depends(get_db)
):

    city_update_validation(
        db=db,
        city_id=city_id,
        new_city_name=new_city_name,
        new_additional_info=new_additional_info,
    )

    city_updated = crud.update_city(
        db=db,
        current_city_id=city_id,
        new_city_name=new_city_name,
        new_additional_info=new_additional_info
    )

    return city_updated
