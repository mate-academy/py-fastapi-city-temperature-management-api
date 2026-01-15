from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import City, CityCreate, CityUpdate
import app.crud as crud

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=City, status_code=status.HTTP_201_CREATED)
def create_city_endpoint(
    city: CityCreate,
    db: Session = Depends(get_db)
):
    return crud.create_city(db, city)


@router.get("/", response_model=list[City])
def get_cities_endpoint(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=City)
def get_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=City)
def update_city_endpoint(
    city_id: int,
    city_update: CityUpdate,
    db: Session = Depends(get_db)
):
    city = crud.update_city(db, city_id, city_update)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    success = crud.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
