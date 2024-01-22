from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from .models import DBCity
from src.dependencies import get_db


def valid_city_id(city_id: int, db: Session = Depends(get_db)) -> DBCity:
    city = db.query(DBCity).filter(DBCity.id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="There are no cities with this id")

    return city
