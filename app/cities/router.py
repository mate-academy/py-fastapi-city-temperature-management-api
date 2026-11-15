from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cities import crud, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
    "", response_model=schemas.City, status_code=status.HTTP_201_CREATED
)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> schemas.City:
    if crud.get_city_by_name(db, city.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )
    return crud.create_city(db, city)


@router.get("", response_model=list[schemas.City])
def list_cities(db: Session = Depends(get_db)) -> list[schemas.City]:
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.City)
def get_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> schemas.City:
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.update_city(db, db_city, city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> None:
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, db_city)
