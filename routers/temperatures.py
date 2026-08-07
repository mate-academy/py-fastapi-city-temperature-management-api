from fastapi import Depends
from sqlalchemy.orm import Session

import crud
import schemas
from main import get_db
from routers.cities import router


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        city_id: int | None = None,
):
    return await crud.get_all_temperature(db, skip=skip, limit=limit, city_id=city_id)

@router.post("/temperatures/update")
async def update_temperatures(
    db: Session = Depends(get_db),
):
    await crud.temperature_update(db)
    return {"message": "Temperatures updated"}


def router():
    return None