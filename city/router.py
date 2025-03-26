from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from city import schemas, crud
from utils import get_db

router = APIRouter()


@router.get("/city/", response_model=list[schemas.City])
def get_city_list(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.post("/city/", response_model=schemas.City)
def create_city(city_data: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city_data=city_data)


@router.put("/city/{city_id}", response_model=schemas.City)
def update_city(city_id: int, updated_city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.update_city(db=db, updated_city=updated_city, city_id=city_id)


@router.patch("/city/{city_id}", response_model=schemas.City)
def partial_update_city(city_id: int, updated_city: schemas.CityUpdate,  db: Session = Depends(get_db)):
    return crud.partial_update_city(db=db, city_id=city_id, updated_city=updated_city)


@router.delete("/city/{city_id}")
def delete_city(city_id: int,  db: Session = Depends(get_db)) -> str:
    return crud.delete_city(city_id=city_id, db=db)
