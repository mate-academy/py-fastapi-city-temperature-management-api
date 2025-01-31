import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.database.models.city import City
from app.database.models.temperature import Temperature
from app.database.session import get_db
from app.schemas.temperature import (
    PaginatedTemperatureResponseSchema,
    TemperatureResponseSchema,
)
from app.services.weather import get_current_temperatures
from services.weather import WeatherAPIError

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_temperatures(db: Session = Depends(get_db)) -> dict[str, str]:
    cities = db.query(City).all()

    if not cities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cities found in the database",
        )

    city_names = [city.name for city in cities]

    async with aiohttp.ClientSession() as session:
        try:
            temperatures = await get_current_temperatures(city_names, session)

            if not temperatures:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to fetch temperature data for any city",
                )
        except WeatherAPIError as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)
            )

    new_records = []

    for city in cities:
        if city.name in temperatures:
            new_record = Temperature(
                city_id=city.id,
                temperature=temperatures[city.name],
            )
            new_records.append(new_record)

    if not new_records:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch temperature data for any city",
        )

    db.add_all(new_records)
    db.commit()

    return {
        "detail": f"Successfully updated temperature data for {len(new_records)} cities"
    }


@router.get("/", response_model=PaginatedTemperatureResponseSchema)
def get_list_of_temperatures(
    request: Request,
    city_id: int | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PaginatedTemperatureResponseSchema:
    query = db.query(Temperature)

    if city_id:
        if not db.query(City).filter_by(id=city_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with id {city_id} not found",
            )
        query = query.filter_by(city_id=city_id)

    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page

    temperatures = (
        query.order_by(Temperature.date_time.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    if not temperatures and page > 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No temperatures found",
        )

    base_url = str(request.base_url) + "temperatures/"

    return PaginatedTemperatureResponseSchema(
        temperatures=[
            TemperatureResponseSchema.model_validate(temp) for temp in temperatures
        ],
        total_items=total_items,
        total_pages=total_pages,
        prev_page=(
            f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
        ),
        next_page=(
            f"{base_url}?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
    )
