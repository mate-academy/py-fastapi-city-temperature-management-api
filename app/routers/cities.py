"""City CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """Create a new city. City names must be unique."""
    if crud.get_city_by_name(db, city.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City '{city.name}' already exists",
        )
    return crud.create_city(db, city)


@router.get("", response_model=list[schemas.City])
def list_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all cities."""
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """Get the details of a specific city."""
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)
):
    """Update the details of a specific city (partial update)."""
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    if city_update.name and city_update.name != db_city.name:
        existing = crud.get_city_by_name(db, city_update.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"City '{city_update.name}' already exists",
            )

    return crud.update_city(db, db_city, city_update)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete a specific city (and its temperature history, via cascade)."""
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, db_city)
    return None
