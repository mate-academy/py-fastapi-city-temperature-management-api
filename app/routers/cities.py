from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(tags=["cities"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.City)
def create(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)

@router.get("/", response_model=list[schemas.City])
def read_all(db: Session = Depends(get_db)):
    return crud.get_cities(db)

@router.get("/{city_id}", response_model=schemas.City)
def read(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.put("/{city_id}", response_model=schemas.City)
def update(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    updated = crud.update_city(db, city_id, city)
    if updated is None:
        raise HTTPException(status_code=404, detail="City not found")
    return updated

@router.delete("/{city_id}", response_model=schemas.City)
def delete(city_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_city(db, city_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="City not found")
    return deleted
