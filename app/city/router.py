from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_city_by_id(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_city


@router.post("/cities/", response_model=schemas.CityCreate)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city=city, city_id=city_id)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted_city = crud.delete_city(db, city_id)
    if deleted_city:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="City not found")
