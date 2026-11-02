from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from city_temp import crud, schemas
from city_temp.database import SessionLocal

router = APIRouter(prefix="/cities", tags=["Cities"])


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


SessionDep = Annotated[Session, Depends(get_db)]


@router.post(
    "/", response_model=schemas.CityResponse, status_code=status.HTTP_201_CREATED
)
def create_city(city: schemas.CityCreate, db: SessionDep):
  return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.CityResponse])
def read_cities(db: SessionDep):
  return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.CityResponse)
def read_city(city_id: int, db: SessionDep):
  db_city = crud.get_city(db, city_id=city_id)
  if db_city is None:
    raise HTTPException(status_code=404, detail="City not found")
  return db_city


@router.put("/{city_id}", response_model=schemas.CityResponse)
def update_city(city_id: int, city: schemas.CityCreate, db: SessionDep):
  db_city = crud.update_city(db=db, city_id=city_id, city_data=city)
  if db_city is None:
    raise HTTPException(status_code=404, detail="City not found")
  return db_city


@router.delete("/{city_id}", response_model=schemas.CityResponse)
def delete_city(city_id: int, db: SessionDep):
  db_city = crud.delete_city(db=db, city_id=city_id)
  if db_city is None:
    raise HTTPException(status_code=404, detail="City not found")
  return db_city
