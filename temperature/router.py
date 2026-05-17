import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from city import crud as city_crud
from city.database import get_db
from temperature import crud, models, schemas, weather

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post(
    "/update",
    response_model=list[schemas.Temperature],
    status_code=status.HTTP_201_CREATED,
)
async def update_temperatures(db: Session = Depends(get_db)) -> list[models.Temperature]:
    cities = city_crud.get_cities(db=db)
    if not cities:
        return []

    created_temperatures = []
    try:
        for city in cities:
            current_temperature = await weather.fetch_current_temperature(city.name)
            created_temperatures.append(
                crud.create_temperature(
                    db=db,
                    city_id=city.id,
                    date_time=current_temperature.date_time,
                    temperature=current_temperature.temperature,
                )
            )
    except (httpx.HTTPError, weather.WeatherFetchError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Could not fetch current temperature: {exc}",
        ) from exc

    return created_temperatures


@router.get("/", response_model=list[schemas.Temperature], include_in_schema=False)
@router.get("", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[models.Temperature]:
    if city_id is not None and city_crud.get_city(db=db, city_id=city_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return crud.get_temperatures(db=db, city_id=city_id)
