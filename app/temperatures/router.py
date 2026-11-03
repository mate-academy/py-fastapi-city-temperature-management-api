from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cities import crud as cities_crud
from app.dependencies import get_db
from app.temperatures import crud, schemas, service

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=schemas.TemperatureUpdateResult)
async def update_temperatures(db: Session = Depends(get_db)):
    cities = cities_crud.get_cities(db, limit=10_000)
    if not cities:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "No cities in the database"
        )

    ok, failed = await service.fetch_all_temperatures(
        [(c.id, c.name) for c in cities]
    )
    if ok:
        crud.create_temperatures(db, ok)
    if not ok:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            f"Could not fetch temperature for any city: {failed}",
        )
    return schemas.TemperatureUpdateResult(updated=len(ok), failed=failed)


@router.get("", response_model=list[schemas.Temperature])
def list_temperatures(
        city_id: int | None = None,
        db: Session = Depends(get_db)
):
    if city_id is not None and cities_crud.get_city(db, city_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "City not found")
    return crud.get_temperatures(db, city_id)
