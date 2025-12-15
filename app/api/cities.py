from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("", response_model=schemas.CityRead, status_code=status.HTTP_201_CREATED)
def create_city(city_in: schemas.CityCreate, db: Session = Depends(get_db)):
    existing = crud.get_city_by_name(db, city_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City with this name already exists",
        )
    return crud.create_city(db, city_in)


@router.get("", response_model=list[schemas.CityRead])
def get_cities(db: Session = Depends(get_db)):
    return crud.list_cities(db)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")

    crud.delete_city(db, city)
    return None
