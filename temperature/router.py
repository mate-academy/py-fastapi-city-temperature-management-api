from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from temperature import schemas
from dependencies import get_db
from temperature.crud import get_temperatures, update_city_temperature
from temperature.models import DBTemperature


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    db: Session = Depends(get_db)
) -> list[schemas.Temperature]:
    temperatures = get_temperatures(db=db, city_id=city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures


@router.put(
    "/temperatures/{temperature_id}/",
    response_model=schemas.Temperature
)
async def update_temperature(
    temperature_id: int,
    db: Session = Depends(get_db)
) -> schemas.Temperature:
    db_temperature = (db.query(DBTemperature)
                      .filter(DBTemperature.id == temperature_id)
                      .first())
    if db_temperature is None:
        raise HTTPException(
            status_code=404,
            detail="Temperature record not found"
        )
    return await update_city_temperature(db=db, db_temperature=db_temperature)
