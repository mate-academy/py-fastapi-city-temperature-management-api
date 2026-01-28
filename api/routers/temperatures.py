import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.deps import get_db
from crud import cities as city_crud
from crud import temperatures as temp_crud
from schemas.temperature import TemperatureRead
from services.weather import WeatherError, fetch_current_temperature_celsius

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

@router.get("", response_model=list[TemperatureRead])
def list_temperatures(
    city_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return temp_crud.list_temperatures(db, city_id=city_id)

@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.list_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database")

    async def fetch_for_city(c):
        try:
            t = await fetch_current_temperature_celsius(c.name)
            return (c.id, t, None)
        except (WeatherError, Exception) as e:
            return (c.id, None, str(e))

    results = await asyncio.gather(*(fetch_for_city(c) for c in cities))

    created = 0
    errors: list[dict] = []

    for city_id, temp, err in results:
        if err is not None:
            errors.append({"city_id": city_id, "error": err})
            continue
        temp_crud.add_temperature(db, city_id=city_id, temp=float(temp))
        created += 1

    return {"created": created, "errors": errors}
