from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..crud import get_cities, create_city

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cities")
def read_cities(db: Session = Depends(get_db)):
    return get_cities(db)

@router.post("/cities")
def add_city(name: str, additional_info: str, db: Session = Depends(get_db)):
    return create_city(db, name, additional_info)