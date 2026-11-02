from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.city import crud, schemas
from src.city.models import City
from src.dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


def get_city_or_404(city_id: int, db: Session = Depends(get_db)) -> City:
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, city.name):
        raise HTTPException(status_code=400, detail="City with this name already exists")
    return crud.create_city(db, city)


@router.get("/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


# optional
@router.get("/{city_id}", response_model=schemas.City)
def read_city(city: City = Depends(get_city_or_404)):
    return city


# optional
@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_data: schemas.CityUpdate,
    city: City = Depends(get_city_or_404),
    db: Session = Depends(get_db),
):
    if city_data.name and city_data.name != city.name:
        if crud.get_city_by_name(db, city_data.name):
            raise HTTPException(status_code=400, detail="City with this name already exists")
    return crud.update_city(db, city, city_data)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city: City = Depends(get_city_or_404), db: Session = Depends(get_db)):
    crud.delete_city(db, city)
