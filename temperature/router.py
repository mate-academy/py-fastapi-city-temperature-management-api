from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature import crud, schemas


router = APIRouter()


@router.get(
    "/temperature/",
    response_model=list[schemas.Temperature]
)
async def get_temperature_list(
        city_id: int = Query(None, description="City id"),
        db: Session = Depends(get_db)
):

    if city_id:
        temperature = await crud.get_temperatures_by_city_id(
            db=db, city_id=city_id
        )
        if not temperature:
            raise HTTPException(status_code=400, detail="Temperature does not exist")

        return [temperature]

    return await crud.get_temperature_list(db=db)


@router.post("/temperature/update/", response_model=dict)
async def update_temperature(db: Session = Depends(get_db)):
    result = await crud.set_temperature(db=db)
    return result
