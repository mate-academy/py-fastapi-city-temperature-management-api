from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud.temperature import (
    get_all_temperatures,
    update_temperatures,
    get_temperatures_by_city
)

temperature_router = APIRouter()


@temperature_router.post("/temperatures/update")
async def update_temperatures_for_all_cities_endpoint(
        db: Session = Depends(get_db)
):
    return await update_temperatures(db)


@temperature_router.get("/temperatures")
def get_all_temperatures_endpoint(db: Session = Depends(get_db)):
    return get_all_temperatures(db)


@temperature_router.get("/temperatures/")
def get_temperatures_by_city_endpoint(
        city_id: int, db: Session = Depends(get_db)
):
    return get_temperatures_by_city(db, city_id=city_id)
