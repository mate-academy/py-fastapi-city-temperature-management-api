from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import crud
from city import schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def get_all_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def get_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(city_id=city_id, db=db)

    if db_city is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.update_city(city_id=city_id, city=city, db=db)

    if db_city is None:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    return db_city


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    is_deleted = crud.delete_city(city_id=city_id, db=db)
    if is_deleted:
        return {"message": "City deleted"}

    return {"message": f"City with id {city_id} not found"}


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)
