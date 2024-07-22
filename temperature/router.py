from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud
router = APIRouter(prefix="/api")

@router.get("/temperatures", response_model=list[schemas.Temperature])
def get_temperature(db: Session = Depends(get_db),skip: int = 0, limit: int = 10):
    temperature = crud.get_all_temperatures(db, skip, limit)
    return temperature


@router.post("/temperatures/update")
async def get_cities(db: Session = Depends(get_db)): 
    return await crud.get_temperatures_for_cities(db)


@router.get("/temperatures/?city_id={city_id}", response_model=schemas.Temperature)
def get_temperature_by_id(city_id: int, db: Session = Depends(get_db)):
    temperature = crud.get_temperature_by_city_id(db, city_id)
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperature
