from fastapi import APIRouter, HTTPException
from database import DbSession
from city.crud import create_city, get_cities, get_city, delete_city
from city.schemas import CityCreate, CityResponse

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=CityResponse)
def create_city_endpoint(city: CityCreate, db: DbSession):
    return create_city(db, city)


@router.get("/", response_model=list[CityResponse])
def get_cities_endpoint(db: DbSession):
    return get_cities(db)


@router.get("/{city_id}", response_model=CityResponse)
def get_city_endpoint(city_id: int, db: DbSession):
    db_city = get_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}", response_model=CityResponse)
def delete_city_endpoint(city_id: int, db: DbSession):
    db_city = delete_city(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
