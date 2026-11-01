from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import City
from app.schemas import CityCreate, CityResponse

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post(
    "/",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_city(city_data: CityCreate, db: Session = Depends(get_db)):
    city = City(**city_data.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@router.get("/", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    db.delete(city)
    db.commit()
