from typing import Any
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.crud.city import get_city


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_city_or_404(
    city_id: int,
    db: Session = Depends(get_db)
) -> Any:
    city = get_city(db, city_id)
    if not city:
        raise HTTPException(404, "City not found")
    return city
