from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature.crud import get_temperatures_crud, check_current_temperatures
from temperature.schemas import TemperatureResponse

router = APIRouter()


@router.get("/temperatures", response_model=list[TemperatureResponse])
def get_temperatures(db: Session = Depends(get_db), city_id: int = None):
    return get_temperatures_crud(db, city_id)


@router.post("/temperatures/update", response_model=list[TemperatureResponse])
async def check_all_city_temperatures(db: Session = Depends(get_db)):
    return await check_current_temperatures(db)
