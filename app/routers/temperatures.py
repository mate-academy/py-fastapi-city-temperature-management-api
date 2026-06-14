from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.models import City, Temperature
from app.services.weather import get_temperature

router = APIRouter(prefix="/temperatures")


@router.post("/update")
async def update_temperatures(
    db: Session = Depends(get_db)
):
    cities = db.query(City).all()

    for city in cities:
        temp = await get_temperature(city.name)

        crud.create_temperature(
            db,
            city.id,
            temp,
            datetime.utcnow()
        )

    return {"message": "updated"}


@router.get("/")
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Temperature)

    if city_id is not None:
        query = query.filter(
            Temperature.city_id == city_id
        )

    return query.all()
