from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import crud, schemas
from database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db)
    if any(c.name == city.name for c in cities):
        raise HTTPException(
            status_code=400,
            detail=f"City with name '{city.name}' already exists"
        )
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    updated = crud.update_city(db=db, city_id=city_id, city=city)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db=db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return deleted
