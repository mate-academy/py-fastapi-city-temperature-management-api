from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import CityCreate, CityResponse, CityUpdate
import app.crud.city as crud

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    """Create a new city. Returns 409 if a city with the same name already exists."""
    existing = crud.get_city_by_name(db, city.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city.name}' already exists.",
        )
    return crud.create_city(db, city)


@router.get("/", response_model=list[CityResponse])
def list_cities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Return a paginated list of all cities."""
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """Return details for a specific city by ID."""
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return db_city


@router.put("/{city_id}", response_model=CityResponse)
def update_city(city_id: int, city_data: CityUpdate, db: Session = Depends(get_db)):
    """Update one or more fields of an existing city."""
    # Check for name collision only when a new name is supplied
    if city_data.name:
        existing = crud.get_city_by_name(db, city_data.name)
        if existing and existing.id != city_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Another city with name '{city_data.name}' already exists.",
            )
    db_city = crud.update_city(db, city_id, city_data)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return db_city


@router.delete("/{city_id}", response_model=CityResponse)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete a city and all its associated temperature records."""
    db_city = crud.delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return db_city