from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.db import get_db
from app.models import City

router = APIRouter()


@router.post("/", response_model=schemas.CityRead, status_code=status.HTTP_201_CREATED)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db)
) -> City:
    existing = crud.get_city_by_name(db, city.name)
    if existing:
        raise HTTPException(status_code=400, detail="City with that name already exists")
    return crud.create_city(db, city)


@router.get("/", response_model=List[schemas.CityRead])
def list_cities(db: Session = Depends(get_db)):
    return crud.list_cities(db)


@router.get("/{city_id}", response_model=schemas.CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.CityRead)
def update_city(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    updated = crud.update_city(db, city_id, city_update)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_city(db, city_id)
    if not ok:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "deleted"}
