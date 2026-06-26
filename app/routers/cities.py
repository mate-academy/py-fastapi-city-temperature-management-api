from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    return db.query(models.City).order_by(models.City.id).all()


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = _get_city_or_404(city_id, db)
    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: Session = Depends(get_db),
):
    city = _get_city_or_404(city_id, db)
    update_data = city_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = _get_city_or_404(city_id, db)
    db.delete(city)
    db.commit()
    return None


def _get_city_or_404(city_id: int, db: Session) -> models.City:
    city = db.get(models.City, city_id)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return city
