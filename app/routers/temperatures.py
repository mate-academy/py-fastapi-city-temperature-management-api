from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_db
from app.services import weather


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


@router.post("/update")
async def update_temperatures(
    db: Session = Depends(get_db)
) -> dict[str, int]:
    updated_count = await weather.update_all_temperatures(db)

    return {"updated": updated_count}


@router.get(
    "",
    response_model=list[schemas.TemperatureRead]
)
@router.get(
    "/",
    response_model=list[schemas.TemperatureRead],
    include_in_schema=False
)
def read_temperatures(
    db: Session = Depends(get_db),
    city_id: int | None = Query(default=None, gt=0)
) -> list[models.Temperature]:
    return crud.get_temperatures(db, city_id=city_id)