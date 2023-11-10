from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
def read_cities(db: Session = Depends(get_db)) -> list[schemas.CityList]:
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.CityList)
def create_city(city: schemas.CityBase, db: Session = Depends(get_db)) -> schemas.CityList:
    db_city = crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(status_code=400, detail="This city already exists")

    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.CityList)
def read_single_city(city_id: int, db: Session = Depends(get_db)) -> schemas.CityList:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=400, detail="City not found")

    return db_city


@router.put("/cities/{city_id}/", response_model=schemas.CityList)
def update_city(city_id: int, city: schemas.CityBase, db: Session = Depends(get_db)) -> schemas.CityList:
    return crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)) -> dict:
    return crud.delete_city(db=db, city_id=city_id)
