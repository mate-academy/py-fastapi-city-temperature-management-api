from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.city import City
from app.schemas.city import CityCreate, CityRead

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post(
    "",
    response_model=CityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_city(
    city_in: CityCreate,
    db: Session = Depends(get_db),
):
    existing_city = db.query(City).filter(City.name == city_in.name).first()
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )

    city = City(**city_in.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)

    return city


@router.get(
    "",
    response_model=list[CityRead],
)
def get_cities(
    db: Session = Depends(get_db),
):
    return db.query(City).all()


@router.get(
    "/{city_id}",
    response_model=CityRead,
)
def get_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )
    return city


@router.put(
    "/{city_id}",
    response_model=CityRead,
)
def update_city(
    city_id: int,
    city_in: CityCreate,
    db: Session = Depends(get_db),
):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    existing_city = db.query(City).filter(
        City.name == city_in.name, City.id != city_id
    ).first()
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists",
        )

    for field, value in city_in.model_dump().items():
        setattr(city, field, value)

    db.commit()
    db.refresh(city)

    return city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    db.delete(city)
    db.commit()
