import datetime
from fastapi import HTTPException

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from temperature_management import models
from temperature_management import schemas


def get_all_cities(
        db: Session
):
    return db.scalars(select(models.DBCity)).all()


def create_city(
        db: Session,
        city_info: schemas.CityCreate
):
    if db.scalar(
            select(
                models.DBCity
            ).where(models.DBCity.name == city_info.name)):
        raise HTTPException(
            status_code=400,
            detail="City with such name already exists!!!"
        )
    db_city = models.DBCity(
        **city_info.model_dump()
    )

    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(
        db: Session,
        city_id: int
):
    db_city = db.get(models.DBCity, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


def update_city(
        db: Session,
        city_id: int,
        city_update_info: schemas.CityUpdate
):
    db_city = db.get(models.DBCity, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    for field, value in city_update_info.model_dump().items():
        setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)

    return db_city


def partial_update_city(
        db: Session,
        city_id: int,
        city_update_info: schemas.CityPartialUpdate
):
    db_city = db.get(models.DBCity, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    city_update_info = city_update_info.model_dump(exclude_unset=True)

    if city_update_info:
        for field, value in city_update_info.items():
            setattr(db_city, field, value)

    db.commit()
    db.refresh(db_city)

    return db_city


def delete_city_by_id(
        db: Session,
        city_id: int
):
    db_city = db.get(models.DBCity, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(db_city)
    db.commit()

    return db_city


async def fetch_temperature(
        db: Session,
):
    cities = db.scalars(select(models.DBCity)).all()
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    f"https://wttr.in/{city.name}?format=j1"
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                print(f"Error for {city.name}: {e}")
                continue
            except httpx.RequestError as e:
                print(f"Error for {city.name}: {e}")
            response = response.json()
            date = datetime.date.today()
            time = response.get(
                "current_condition"
            )[0].get("observation_time")
            date_time = datetime.datetime.strptime(
                f"{date} {time}", "%Y-%m-%d %I:%M %p")
            if not db.scalar(select(
                    models.DBTemperature
            ).where(
                models.DBTemperature.city_id == city.id,
                models.DBTemperature.date_time == date_time
            )):
                new_temperature = models.DBTemperature(
                    temperature=response.get(
                        "current_condition"
                    )[0].get("temp_C"),
                    city_id=city.id,
                    date_time=date_time
                )

                db.add(new_temperature)
                db.flush()
    db.commit()


def get_all_temperatures(db: Session):
    return db.scalars(select(models.DBTemperature)).all()


def get_temperatures_by_id(
        db: Session,
        city_id: int
):
    db_city = db.get(models.DBCity, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    response = {"city": f"{db_city.name}"}
    temperatures = db.scalars(
        select(
            models.DBTemperature
        ).where(models.DBTemperature.city_id == city_id)).all()
    if not temperatures:
        return {"city": f"{db_city.name}", "temperatures": []}
    response["temperatures"] = temperatures

    return response
