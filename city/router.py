from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from dependencies import get_db
from city.schemas import CityCreate, CityRead
from city.crud import create_city, delete_city, get_cities_list

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=CityRead)
def create_city_endpoint(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db, city)


@router.delete("/{city_id}")
def delete_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    result = delete_city(db, city_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/")
def read_cities(db: Session = Depends(get_db)):
    return get_cities_list(db)
