from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.city import crud as city_crud
from app.database import get_db
from app.temperature import crud, schemas, service

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update", response_model=list[schemas.Temperature])
async def update_temperatures(db: Session = Depends(get_db)):
    cities = city_crud.get_cities(db, limit=1000)
    if not cities:
        return []
    temperatures = await service.fetch_temperatures(cities)
    if not temperatures:
        return []
    return crud.create_temperatures(db, temperatures)


@router.get("", response_model=list[schemas.Temperature])
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(db, city_id=city_id, skip=skip, limit=limit)
