from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=schemas.City)
def create(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@router.get("/", response_model=list[schemas.City])
def read_all(db: Session = Depends(get_db)):
    return crud.get_cities(db)


@router.delete("/{city_id}")
def delete(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "Deleted"}
