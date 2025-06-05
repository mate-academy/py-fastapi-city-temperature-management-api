from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.city import crud, schemas
from app.depencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[schemas.City])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db=db, id_city=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db=db, id_city=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted successfully"}
