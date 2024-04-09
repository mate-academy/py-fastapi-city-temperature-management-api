from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_city(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
):
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
def detail_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    city = crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityBase,
        db: Session = Depends(get_db)

):
    city = crud.update_city(db=db, city_id=city_id, city=city)
    if city is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return city


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)

):
    city = crud.delete_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return city
