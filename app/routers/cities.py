from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import crud, schemas, deps


router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.CityRead, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(deps.get_db)):
    existing = db.query(crud.models.City).filter(crud.models.City.name == city.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City with this name already exists")
    try:
        return crud.create_city(db, city)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City with this name already exists")


@router.get("/", response_model=list[schemas.CityRead])
def read_cities(db: Session = Depends(deps.get_db)):
    return crud.get_cities(db)


@router.delete("/{city_id}", response_model=schemas.CityRead)
def delete_city(city_id: int, db: Session = Depends(deps.get_db)):
    city = crud.delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city
