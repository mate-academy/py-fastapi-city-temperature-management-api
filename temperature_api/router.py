import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city_api.crud import get_cities
from dependencies import get_db
from temperature_api import crud, schemas
import httpx

load_dotenv()

router = APIRouter()


@router.get("/temperature/", response_model=list[schemas.TemperatureBase])
def read_temperature(city_id: int = None, db: Session = Depends(get_db)):
    return crud.cities_temperatures(db=db, city_id=city_id)


@router.post("/temperature/update/")
async def update_temperature_database(db: Session = Depends(get_db)):
    cities = get_cities(db=db)
    if cities:
        async with httpx.AsyncClient() as client:
            for city in cities:
                kwargs = {"key": os.getenv("APIKEY"), "q": city.name}
                try:
                    response = await client.get(
                        os.getenv("URL"),
                        params=kwargs
                    )
                    response.raise_for_status()
                    data = response.json()
                    temperature = data["current"]["temp_c"]
                    crud.update_city_temperature(
                        db=db,
                        city_id=city.id,
                        temperature=temperature
                    )
                except httpx.HTTPError as error:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Page not found for city - {city.name}\n"
                               f"Error: {error}",
                    )
                except Exception as error:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Can't update temperature for {city.name}\n"
                               f"Error: {error}"
                    )
        return {"message": "Updated successfully"}
    else:
        return {"message": "Cities not found in DB"}
