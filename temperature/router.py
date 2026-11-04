from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud as city_crud
from dependencies import get_db
from temperature import crud, schemas, service

router = APIRouter(tags=["temperatures"])


@router.post("/temperatures/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await city_crud.get_all_cities(db)
    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities in the database"
        )

    temperatures = await service.fetch_temperatures(cities)
    if not temperatures:
        raise HTTPException(
            status_code=502,
            detail="Could not fetch temperature data"
        )

    records = await crud.create_temperatures(db, temperatures)
    return {"updated": len(records), "skipped": len(cities) - len(records)}


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def list_temperatures(
    city_id: int | None = None, db: AsyncSession = Depends(get_db)
):
    if city_id is not None and await city_crud.get_city(db, city_id) is None:
        raise HTTPException(status_code=404, detail="City not found")
    return await crud.get_temperatures(db, city_id=city_id)
