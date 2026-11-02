from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
import httpx
from sqlalchemy.orm import Session
from city_temp import crud, schemas
from city_temp.database import SessionLocal

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


SessionDep = Annotated[Session, Depends(get_db)]


async def fetch_weather_for_city(client: httpx.AsyncClient, city_name: str):
  geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
  geo_res = await client.get(geo_url)
  geo_data = geo_res.json()

  if "results" not in geo_data or not geo_data["results"]:
    return None

  location = geo_data["results"][0]
  lat = location["latitude"]
  lon = location["longitude"]

  weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
  weather_res = await client.get(weather_url)
  weather_data = weather_res.json()

  return weather_data.get("current", {}).get("temperature_2m")


@router.post("/update", status_code=201)
async def update_temperatures(db: SessionDep):
  cities = crud.get_cities(db)
  if not cities:
    raise HTTPException(
        status_code=404, detail="No cities found in database to update."
    )

  updated_count = 0
  async with httpx.AsyncClient() as client:
    for city in cities:
      temp = await fetch_weather_for_city(client, city.name)
      if temp is not None:
        crud.create_temperature_record(db=db, city_id=city.id, temperature=temp)
        updated_count += 1

  return {
      "message": (
          f"Successfully fetched and stored temperatures for {updated_count}"
          " cities."
      )
  }


@router.get("/", response_model=list[schemas.TemperatureResponse])
def get_temperatures(
    city_id: int | None = Query(None, description="Filter by city ID"),
    db: SessionDep = Depends(get_db),
):
  return crud.get_temperatures(db, city_id=city_id)
