from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)


@router.post("/", response_model=schemas.CityResponse,
             status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate,
                db: Session = Depends(database.get_db)) -> models.City:
    db_city = db.query(models.City).filter(
        models.City.name == city.name).first()
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")

    new_city = models.City(name=city.name,
                           additional_info=city.additional_info)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.get("/", response_model=List[schemas.CityResponse])
def get_cities(db: Session = Depends(database.get_db)) -> List[models.City]:
    return db.query(models.City).all()


@router.get("/{city_id}", response_model=schemas.CityResponse)
def get_city(city_id: int, db: Session = Depends(database.get_db)) -> models.City:
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.CityResponse)
def update_city(city_id: int, updated_city: schemas.CityUpdate,
                db: Session = Depends(database.get_db)) -> models.City:
    city_query = db.query(models.City).filter(models.City.id == city_id)
    city = city_query.first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city_query.update(updated_city.model_dump(), synchronize_session=False)
    db.commit()
    return city_query.first()


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(database.get_db)) -> None:
    city_query = db.query(models.City).filter(models.City.id == city_id)
    city = city_query.first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city_query.delete(synchronize_session=False)
    db.commit()
    return None