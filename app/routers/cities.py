from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


def get_city_or_404(city_id: int, db: Session) -> models.City:
    city = db.get(models.City, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)) -> models.City:
    record = models.City(**city.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="City name already exists") from exc
    db.refresh(record)
    return record


@router.get("", response_model=list[schemas.City])
def list_cities(db: Session = Depends(get_db)) -> list[models.City]:
    return list(db.scalars(select(models.City).order_by(models.City.id)))


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)) -> models.City:
    return get_city_or_404(city_id, db)


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)
) -> models.City:
    record = get_city_or_404(city_id, db)
    for field, value in city.model_dump().items():
        setattr(record, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="City name already exists") from exc
    db.refresh(record)
    return record


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> Response:
    db.delete(get_city_or_404(city_id, db))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
