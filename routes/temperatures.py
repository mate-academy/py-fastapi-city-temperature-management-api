import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from crud import get_temperatures, create_temperature, get_cities
from schemas import TemperatureResponse

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.get("/", response_model=list[TemperatureResponse])
def list_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_temperatures(db, city_id)


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = get_cities(db)

    created = []
    for city in cities:
        fake_temperature = round(random.uniform(-10, 35), 2)

        temp = create_temperature(
            db=db,
            city_id=city.id,
            temperature=fake_temperature,
        )
        created.append(temp)

    return {"detail": f"Temperatures updated for {len(created)} cities"}
