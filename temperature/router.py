from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from temperature import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.post("/temperatures/update/")
async def update_city_temperatures(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
) -> None:
    await crud.update_temperatures(db, background_tasks)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[schemas.Temperature]:
    temperatures = crud.get_temperatures(db, skip=skip, limit=limit)
    return temperatures


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
def read_temperature(
        city_id: int,
        db: Session = Depends(get_db)
) -> schemas.Temperature:
    db_temperature = crud.get_temperature(db, city_id=city_id)
    if db_temperature is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_temperature
