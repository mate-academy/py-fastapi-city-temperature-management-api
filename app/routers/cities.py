from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import DbSession


router = APIRouter(prefix="/cities", tags=["cities"])


def get_city_or_404(db: Session, city_id: int) -> models.City:
    city = db.get(models.City, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


def commit_or_409(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="A city with this name already exists"
        )


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: DbSession) -> models.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    commit_or_409(db)
    db.refresh(db_city)
    return db_city


@router.get("", response_model=list[schemas.City])
def get_cities(db: DbSession) -> list[models.City]:
    return list(db.scalars(select(models.City)).all())


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: DbSession) -> models.City:
    return get_city_or_404(db, city_id)


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.CityCreate, db: DbSession
) -> models.City:
    db_city = get_city_or_404(db, city_id)
    db_city.name = city.name
    db_city.additional_info = city.additional_info
    commit_or_409(db)
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: DbSession) -> None:
    db_city = get_city_or_404(db, city_id)
    db.delete(db_city)
    db.commit()
