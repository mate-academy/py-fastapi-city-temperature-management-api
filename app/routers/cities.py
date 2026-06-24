from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=schemas.CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """Create a new city. City names must be unique."""
    existing = crud.get_city_by_name(db, city.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city.name}' already exists.",
        )
    return crud.create_city(db, city)


@router.get("/", response_model=list[schemas.CityResponse])
def list_cities(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Return a paginated list of all cities."""
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """Return details for a single city by ID."""
    db_city = crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return db_city


@router.put("/{city_id}", response_model=schemas.CityResponse)
def update_city(city_id: int, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    """Partially update a city's fields (PATCH semantics via PUT)."""
    if city_update.name:
        conflict = crud.get_city_by_name(db, city_update.name)
        if conflict and conflict.id != city_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"City with name '{city_update.name}' already exists.",
            )
    updated = crud.update_city(db, city_id, city_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return updated


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Delete a city and all its associated temperature records."""
    deleted = crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
