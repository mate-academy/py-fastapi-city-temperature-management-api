from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from database import SessionLocal
from dependencies import get_db
from temperature import schemas, crud
from temperature.crud import update_temperatures

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def temperatures_list(db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db)


@router.get(
    "/temperatures/{city_id}/", response_model=list[schemas.Temperature]
)
def temperatures_list(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperatures_by_city(db=db, city_id=city_id)


@router.post("/temperatures/update/")
def trigger_temperature_update(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_temperatures, db=SessionLocal())
    return {"message": "Temperature update process triggered."}
