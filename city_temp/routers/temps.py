import asyncio
from datetime import datetime
from typing import List, Literal

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependencies
from city_temp import crud
from city_temp.schemas import Temperature
from city_temp.utils import (
    get_coords,
    get_current_temp
)


router = APIRouter(prefix="/temperatures", tags=["temperatures"],)


@router.post("/update/", response_model=dict[str, int])
async def refresh_temperatures(
        db: Session = Depends(dependencies.get_db)
):
    cities = crud.list_cities(db=db)

    sem = asyncio.Semaphore(10)

    async with httpx.AsyncClient(timeout=10) as client:

        async def fetch_one(city) -> (
                tuple[int, datetime, float]
                | Literal["skipped", "error"]
        ):
            async with sem:
                try:
                    coords = await get_coords(client, city.name)
                    if coords is None:
                        return "skipped"

                    cur_time, cur_temp = await get_current_temp(
                        client, *coords
                    )

                    return (
                        city.id,
                        datetime.fromisoformat(cur_time),
                        cur_temp
                    )

                except httpx.HTTPError as ex:
                    print(
                        f"Temp fetch failed "
                        f"for {city.name}: {ex}"
                    )
                    return "error"

        results = await asyncio.gather(
            *(fetch_one(c) for c in cities)
        )

    created = 0
    errors = 0
    skipped = 0

    for result in results:
        if result == "error":
            errors += 1
            continue

        if result == "skipped":
            skipped += 1
            continue

        city_id, dt, temp = result
        crud.add_temperature(
            db=db,
            city_id=city_id,
            date_time=dt,
            temperature=temp
        )
        created += 1

    db.commit()
    return {
        "temp_updated": 1,
        "records_added": created,
        "skipped": skipped,
        "errors": errors,
    }


@router.get("/", response_model=List[Temperature])
def list_temperatures(
        city_id: int | None = None,
        db: Session = Depends(dependencies.get_db)
):
    if city_id is None:
        return crud.list_temperatures(db=db)
    crud.get_city(db=db, city_id=city_id)
    return crud.list_city_temperatures(
        db=db,
        city_id=city_id
    )
