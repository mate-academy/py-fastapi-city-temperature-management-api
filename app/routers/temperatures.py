import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas
from ..services.weather import fetch_current_temperature, WeatherError

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[schemas.TemperatureRead])
def list_temperatures(
    city_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.list_temperatures(db, city_id=city_id)


@router.post("/update", response_model=list[schemas.TemperatureUpdateResult])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.list_cities(db)
    if not cities:
        raise HTTPException(status_code=400, detail="No cities in database. Add cities first.")

    async def fetch_one(city):
        """Fetch temperature for a single city (async I/O only).

        IMPORTANT: do not touch the DB session here because this coroutine is executed
        concurrently across many tasks and SQLAlchemy Session is not concurrency-safe.
        """
        try:
            temp = await fetch_current_temperature(city.name)
            return (city, temp, None)
        except (WeatherError, Exception) as e:
            return (city, None, str(e))

    # 1) Run all external calls concurrently
    fetched = await asyncio.gather(*(fetch_one(c) for c in cities))

    # 2) Persist results in a single, sequential DB transaction
    ok_items: list[tuple[int, float]] = []
    results: list[schemas.TemperatureUpdateResult] = []

    for city, temp, err in fetched:
        if err is None and temp is not None:
            ok_items.append((city.id, temp))
            results.append(
                schemas.TemperatureUpdateResult(
                    city_id=city.id,
                    city_name=city.name,
                    ok=True,
                    temperature=temp,
                )
            )
        else:
            results.append(
                schemas.TemperatureUpdateResult(
                    city_id=city.id,
                    city_name=city.name,
                    ok=False,
                    error=err or "Unknown error",
                )
            )

    if ok_items:
        crud.create_temperatures_bulk(db, ok_items)

    return results