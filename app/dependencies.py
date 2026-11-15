from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models
from app.database import get_db

DbSession = Annotated[Session, Depends(get_db)]


def get_city_or_404(city_id: int, db: DbSession) -> models.City:
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with id={city_id} not found",
        )
    return city


CityDep = Annotated[models.City, Depends(get_city_or_404)]
