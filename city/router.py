from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):

    db_city = crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name for City already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):

    cities = crud.get_all_cities(db=db)

    return cities


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_city_by_id(city_id: int, db: Session = Depends(get_db)):

    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city_by_id(
        city: schemas.CityCreate,
        city_id: int,
        db: Session = Depends(get_db)
):

    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.update_city_by_id(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}/")
def delete_city_by_id(city_id: int, db: Session = Depends(get_db)):

    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.delete_city_by_id(db=db, city_id=city_id)
