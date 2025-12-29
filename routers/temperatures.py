from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

import crud
from database import get_db
from schema import TemperatureRead
from services.weather import get_coordinates, fetch_temperature

router = APIRouter()

@router.post("/update")
async def update_temperature(db: Session = Depends(get_db)):
    cities = crud.get_all_cities(db)

    for city in cities:
        lat, lon = await get_coordinates(city.name)
        if lat is None or lon is None:
            continue

        temp = await fetch_temperature(lat, lon)
        crud.add_temperature_to_session(db, city.id, temp)
    db.commit()
    return {"status": "success"}


@router.get("/", response_model=list[TemperatureRead])
async def get_temperature(
        db: Session = Depends(get_db),
        city_id: int | None = None,
):
    if city_id:
        city = crud.get_city_by_id(city_id, db)
        if not city:
            raise HTTPException(status_code=404, detail="City not found")
        return crud.get_city_temperature_list(db, city_id)
    return crud.get_temperature_list(db)
