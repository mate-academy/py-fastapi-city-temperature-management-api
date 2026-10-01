from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas, services
from app.database import get_db

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db, limit=1000)
    if not cities:
        return {"message": "No cities found in database to update."}

    city_map = {city.name: city.id for city in cities}
    results = await services.fetch_temperatures_concurrently(
        list(city_map.keys())
    )

    created_records = []
    failed_cities = []

    for city_name, temp in results.items():
        if temp is not None:
            city_id = city_map[city_name]
            record = crud.create_temperature_record(
                db, city_id=city_id, temp_value=temp
            )
            created_records.append(record)
        else:
            failed_cities.append(city_name)

    return {
        "message": f"Successfully updated temperatures for {len(created_records)} cities.",
        "updated_records_count": len(created_records),
        "failed_cities": failed_cities,
    }


@router.get("", response_model=List[schemas.Temperature])
def read_temperatures(
    city_id: Optional[int] = Query(
        None, description="Filter temperature records by specific city ID"
    ),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None:
        db_city = crud.get_city(db, city_id=city_id)
        if not db_city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with ID {city_id} does not exist.",
            )

    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
