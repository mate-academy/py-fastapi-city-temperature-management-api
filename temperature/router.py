import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.crud import get_cities
from dependencies import get_db
from temperature import crud, schemas
import httpx

load_dotenv()

router = APIRouter()


@router.get("/temperature/", response_model=list[schemas.TemperatureBase])
def read_temperature(city_id: int = None, db: Session = Depends(get_db)):
    return crud.cities_temperatures(db=db, city_id=city_id)


@router.post("/temperature/update/")
async def update_temperature_database(db: Session = Depends(get_db)):
    cities = get_cities(db=db)

    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in the database.")

    async with httpx.AsyncClient() as client:
        for city in cities:
            params = {
                "key": os.getenv("API_KEY"),
                "q": city.name
            }

            try:
                response = await client.get(os.getenv("URL"), params=params)
                response.raise_for_status()

                data = response.json()
                temperature = data["current"]["temp_c"]

                crud.update_city_temperature(
                    db=db,
                    city_id=city.id,
                    temperature=temperature
                )

            except httpx.HTTPStatusError as error:
                raise HTTPException(
                    status_code=error.response.status_code,
                    detail=f"Error fetching data for city '{city.name}': {str(error)}"
                )
            except Exception as error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to update temperature for city '{city.name}'. Error: {str(error)}"
                )

    return {"message": "Temperature updated successfully for all cities."}
