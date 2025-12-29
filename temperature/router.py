from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from dependencies import get_db
from temperature.schemas import TemperatureRead, TemperatureCreate
from temperature.crud import (create_temperatures,
                              get_temperatures_list,
                              get_temperature_by_city_id,
                              update_temperature_for_all_cities)
router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("/", response_model=list[TemperatureRead] | TemperatureRead)
def read_temperatures(
        city_id: int | None = Query(..., description="ID City to filter temperatures"),
        db: Session = Depends(get_db)):
    if city_id:
        city_data = get_temperature_by_city_id(db, city_id)
        if not city_data:
            raise HTTPException(
                status_code=404,
                detail="City not found"
            )
        return city_data
    return get_temperatures_list(db)


@router.post("/create", response_model=TemperatureRead)
def create_temperature_endpoint(
        temperature: TemperatureCreate,
        db: Session = Depends(get_db)
):
    return create_temperatures(db, temperature)


@router.post("/update")
async def update_temperature_endpoint(db: Session = Depends(get_db)):
    result = await update_temperature_for_all_cities(db)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No temperatures were updated"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
