from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.cities.models import City
from app.cities.schemas import CityCreate, CityResponse

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post(
    "/", response_model=CityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_city(city_data: CityCreate, db: Session = Depends(get_db)):
    query = select(City).where(City.name == city_data.name)
    existing_city = db.execute(query).scalar_one_or_none()
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists"
        )

    db_city = City(
        name=city_data.name, additional_info=city_data.additional_info
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@router.get("/", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    query = select(City)
    cities = db.execute(query).scalars().all()
    return cities


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.get(City, city_id)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return db_city


@router.put("/{city_id}", response_model=CityResponse)
def update_city(
        city_id: int,
        city_data: CityCreate,
        db: Session = Depends(get_db)
):
    db_city = db.get(City, city_id)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    db_city.name = city_data.name
    db_city.additional_info = city_data.additional_info
    db.commit()
    db.refresh(db_city)
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.get(City, city_id)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    db.delete(db_city)
    db.commit()
    return None
