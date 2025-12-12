from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import City, Temperature
from app.services.weather import fetch_many

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("/", response_model=schemas.TemperatureHistoryResponse)
def list_temperatures(city_id: Optional[int] = Query(None, description="Filter by city id"), db: Session = Depends(get_db)):
    query = db.query(Temperature).order_by(Temperature.date_time.desc())

    if city_id is not None:
        city_exists = db.get(City, city_id)
        if not city_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
        query = query.filter(Temperature.city_id == city_id)

    records = query.all()
    return schemas.TemperatureHistoryResponse(records=records, total=len(records))


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(City).order_by(City.id.asc()).all()
    if not cities:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cities in database to update.")

    results = await fetch_many([city.name for city in cities])
    now = datetime.utcnow()

    inserted = 0
    failed = 0
    skipped = 0

    for city, result in zip(cities, results):
        if isinstance(result, Exception):
            failed += 1
            continue
        if result is None:
            skipped += 1
            continue

        db.add(Temperature(city_id=city.id, date_time=now, temperature=float(result)))
        inserted += 1

    db.commit()

    message = "Temperature update completed."
    if failed:
        message += f" {failed} cities failed during fetch."
    if skipped:
        message += f" {skipped} cities were skipped."

    return schemas.TemperatureUpdateResult(
        inserted=inserted,
        failed=failed,
        skipped=skipped,
        message=message,
    )

