from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature import schemas, crud
from temperature.models import Temperature
from temperature.utils import update_temperatures

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
        db: Session = Depends(get_db),
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 10
) -> list[Temperature]:
    return crud.get_all_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )


@router.post("/temperatures/", response_model=schemas.Temperature)
def create_temperature(
    temperature: schemas.TemperatureCreate,
    db: Session = Depends(get_db),
) -> Temperature:
    return crud.create_temperature(db=db, temperature=temperature)


@router.post("/temperatures/update/")
async def trigger_update_temperatures(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    background_tasks.add_task(update_temperatures, db=db)
    return {"message": "Temperature update triggered."}
