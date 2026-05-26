from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from . import crud, schemas, services
from city import models as city_models

router = APIRouter()


@router.get(
    "/temperatures/", response_model=list[schemas.TemperatureResponse]
)
def get_temperatures(
        city_id: int | None = None, db: Session = Depends(get_db)
):
    return crud.get_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(city_models.City).all()
    results = []
    for city in cities:
        temp = await services.fetch_temperature(city.name)

        obj = crud.create_temperature(
            db=db,
            temperature=schemas.TemperatureCreate(
                city_id=city.id,
                temperature=temp
            )
        )
        results.append(obj)

    return results
