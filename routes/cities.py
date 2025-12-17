from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from schemas import CityCreate, CityResponse
from crud import (
    create_city,
    get_cities,
    delete_city,
)

router = APIRouter(prefix="/cities")


@router.post("/", response_model=CityResponse)
def create_city_endpoint(
    city_data: CityCreate,
    db: Session = Depends(get_db),
):
    return create_city(db, city_data)


@router.get("/", response_model=list[CityResponse])
def list_cities(
    db: Session = Depends(get_db),
):
    return get_cities(db)


@router.delete("/{city_id}")
def delete_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db),
):
    city = delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "Deleted"}
