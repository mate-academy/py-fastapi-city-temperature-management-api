from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.database import get_db
from app.cities import schemas, crud

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post(
    "/", response_model=schemas.City, status_code=status.HTTP_201_CREATED
)
def create_city(
    city: schemas.CityCreate, db: Annotated[Session, Depends(get_db)]
):
    if crud.get_city_by_name(db, name=city.name):
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )
    return crud.create_city(db, city)


@router.get("/", response_model=List[schemas.City])
def read_cities(db: Annotated[Session, Depends(get_db)]):
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Annotated[Session, Depends(get_db)]):
    db_city = crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    db_city = crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.update_city(db, db_city, city_update)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Annotated[Session, Depends(get_db)]):
    db_city = crud.get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, db_city)
