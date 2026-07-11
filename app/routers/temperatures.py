from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db
from app.services.weather import get_current_temperature

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)


@router.post("/update")
async def update_temperatures(
    db: Session = Depends(get_db),
):
    cities = crud.get_cities(db)

    result = []

    for city in cities:
        temperature = await get_current_temperature(city.name)

        record = crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=temperature,
        )

        result.append(record)

    return result


@router.get("/", response_model=list[schemas.TemperatureResponse])
def get_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(
        db=db,
        city_id=city_id,
    )
