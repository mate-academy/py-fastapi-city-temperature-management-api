from datetime import datetime

from sqlalchemy.orm import Session
import asyncio
from fastapi import HTTPException

from app.crud.city import get_city_by_id_or_404, get_cities
from app.models.temperature import Temperature
from app.external_services.temperature_api import fetch_temperature


async def update_temperatures(db: Session):
    cities = get_cities(db)
    if not cities:
        raise HTTPException(
            status_code=404, detail="There are no cities in the database yet"
        )

    tasks = [fetch_temperature(city.name) for city in cities]
    temperatures = await asyncio.gather(*tasks, return_exceptions=True)

    errors = []
    updated_cities = 0

    for city, result in zip(cities, temperatures):
        if isinstance(result, Exception):
            errors.append(result)
        else:
            new_record = Temperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=result
            )
            db.add(new_record)
            updated_cities += 1

    db.commit()

    if updated_cities == 0:
        raise HTTPException(
            status_code=404,
            detail="No temperature records updated for any city"
        )

    return {
        "message": f"Temperatures updated for {updated_cities} cities",
        "errors": errors
    }


def get_all_temperatures(db: Session):
    temperatures = db.query(Temperature).all()
    if not temperatures:
        raise HTTPException(
            status_code=404, detail="There are no temperature records yet"
        )
    return temperatures


def get_temperatures_by_city(db: Session, city_id: int):
    get_city_by_id_or_404(db=db, city_id=city_id)
    temperatures = db.query(Temperature).filter(
        Temperature.city_id == city_id
    ).all()
    if not temperatures:
        raise HTTPException(
            status_code=404, detail="There are no temperature records yet"
        )
    return temperatures
