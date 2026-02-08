from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import crud, schemas

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_cities(cities: schemas.CityCreate, db: Session = Depends(get_db)):
    exiting = crud.get_city_by_name(db=db, name=cities.name)
    if exiting:
        raise HTTPException(status_code=400, detail="City already exists")
    return crud.create_city(db=db, city=cities)


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    exiting_city = crud.get_city_by_id(db, city_id)
    if exiting_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.update_city(db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}", response_model=schemas.CityDelete)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    crud.delete_city(db, city_id)
    return schemas.CityDelete(id=city_id, deleted=True)
