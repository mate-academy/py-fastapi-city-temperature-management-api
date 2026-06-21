import datetime

import httpx
from fastapi import APIRouter, HTTPException, status

from temperature import crud as temp_crud, schemas
from city import crud as city_crud
from dependencies import DBDep
from temperature import services

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
    db: DBDep,
    city_id: int | None = None,
):
    return await temp_crud.get_all_temperatures(
        db=db,
        city_id=city_id,
    )


@router.post("/temperatures/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: DBDep):
    cities = await city_crud.get_all_cities(db)

    if not cities:
        return {"message": "No cities found in the database to update temperatures."}

    prepared_data = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                lat, lon = await services.fetch_coordinates(client, city.name)

                if lat is None or lon is None:
                    print(f"Coordinates not found for city: {city.name}")
                    continue

                current_temp = await services.fetch_weather_by_coords(client, lat, lon)

                prepared_data.append({
                    "city_id": city.id,
                    "temperature": current_temp,
                    "date_time": datetime.datetime.now()
                })
            except Exception as e:
                print(f"Error updating weather for {city.name} (ID: {city.id}): {e}")
                continue

    created_count = await temp_crud.create_temperature_records(db, prepared_data)

    if created_count > 0:
        return {
            "status": "success",
            "message": f"Successfully updated temperature for {created_count} cities."
        }

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to update data for any city."
    )
