from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from cities import crud as cities_crud
from temperatures import crud, schemas, service

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post(
    "/update",
    response_model=list[schemas.Temperature],
    status_code=status.HTTP_200_OK,
)
async def update_temperatures_for_all_cities(db: Session = Depends(get_db)):
    cities = cities_crud.get_cities(db=db, skip=0, limit=1000)
    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in database to update temperatures.",
        )

    created_temperatures = []

    for city in cities:
        current_temp = await service.fetch_temperature_for_city(city.name)
        if current_temp is not None:
            temp_create = schemas.TemperatureCreate(
                city_id=city.id,
                temperature=current_temp,
            )
            saved_temp = crud.create_temperature(db=db, temperature=temp_create)
            created_temperatures.append(saved_temp)

    return created_temperatures


@router.get("/", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None:
        db_city = cities_crud.get_city(db, city_id=city_id)
        if not db_city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

    return crud.get_temperatures(db=db, skip=skip, limit=limit, city_id=city_id)