from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db=db)


@router.get(
    "/temperatures/{city_id}", response_model=list[schemas.Temperature]
)
def read_temperature_by_city(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperatures_by_city(db=db, city_id=city_id)


@router.post("/temperatures/update", response_model=schemas.UpdateResponse)
def update_temperatures(db: Session = Depends(get_db)):
    try:
        crud.fetch_temperature_data(db)
        return {"message": "Successful update"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed. {e}")
