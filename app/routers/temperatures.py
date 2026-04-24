from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import httpx, asyncio
from .. import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)

    async def fetch_temp(city_name: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"https://wttr.in/{city_name}?format=%t")
            # формат відповіді: "+15°C"
            return float(resp.text.strip().replace("°C", "").replace("+", ""))

    tasks = [fetch_temp(city.name) for city in cities]
    results = await asyncio.gather(*tasks)

    for city, temp_value in zip(cities, results):
        temp = schemas.TemperatureCreate(
            city_id=city.id,
            date_time=datetime.utcnow(),
            temperature=temp_value
        )
        crud.create_temperature(db, temp)

    return {"status": "updated"}

@router.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperatures(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)
