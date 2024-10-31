from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_temperatures(db=db, city_id=city_id)


# @router.get(
#     "/temperatures/{temperature_id}/",
#     response_model=schemas.TemperatureRetrieve
# )
# async def read_temperature(
#         temperature_id: int,
#         db: AsyncSession = Depends(get_db)
# ):
#     return await crud.get_temperature(db=db, temperature_id=temperature_id)


@router.post("/temperatures/update/")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_all_cities(db)
    await crud.fetch_and_store_temperatures(db, cities)
    return {"message": "Temperature data updated"}


@router.delete("/temperatures/{temperature_id}/", response_model=dict)
async def remove_temperature(
    temperature_id: int,
    db: AsyncSession = Depends(get_db),
):
    is_delete = await crud.delete_temperature(
        db=db,
        temperature_id=temperature_id
    )
    if not is_delete:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return {"message": "Temperature deleted"}
