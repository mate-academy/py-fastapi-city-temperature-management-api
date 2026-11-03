from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature import crud
from temperature.schemas import TemperatureRead


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
  created_count = await crud.update_temperatures_for_all_cities(db)
  return {
      "message": f"Successfully updated temperatures for {created_count} cities"
  }


@router.get("/", response_model=list[TemperatureRead])
def get_temperature_by_city(city_id: int | None = None, db: Session = Depends(get_db)):
    if city_id is not None:
        return crud.get_temperature_by_city_id(db, city_id)
    return crud.get_all_temperatures(db)