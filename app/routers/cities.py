"""City CRUD endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter(prefix="/cities", tags=["cities"])
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_city_or_404(city_id: int, db: Session) -> models.City:
    city = db.get(models.City, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(payload: schemas.CityCreate, db: DatabaseSession) -> models.City:
    city = models.City(**payload.model_dump())
    db.add(city)
    try:
        db.commit()
        db.refresh(city)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create city",
        ) from exc
    return city


@router.get("", response_model=list[schemas.City])
def list_cities(db: DatabaseSession) -> list[models.City]:
    return list(db.scalars(select(models.City).order_by(models.City.id)))


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: DatabaseSession) -> models.City:
    return get_city_or_404(city_id, db)


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    payload: schemas.CityUpdate,
    db: DatabaseSession,
) -> models.City:
    city = get_city_or_404(city_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(city, field, value)

    try:
        db.commit()
        db.refresh(city)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update city",
        ) from exc
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: DatabaseSession) -> Response:
    city = get_city_or_404(city_id, db)
    db.delete(city)
    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete city",
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
