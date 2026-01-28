from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from . import crud, schemas

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityRead])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_one_city(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found.")

    return db_city


@router.post("/cities/", response_model=schemas.CityRead)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    existing_city = crud.get_city_by_name(db=db, city_name=city.name)

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exists."
        )

    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.CityRead)
def update_city(city_id: int, city_data: schemas.CityUpdate, db: Session = Depends(get_db)):
    updated_city = crud.update_city(db=db, city_id=city_id, city_data=city_data)

    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found.")

    return updated_city


@router.delete("/cities/{city_id}/", response_model=schemas.CityRead)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = crud.delete_city(db=db, city_id=city_id)

    if not deleted_city:
        raise HTTPException(status_code=404, detail="City not found.")

    return deleted_city
