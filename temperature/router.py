from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from dependencies import get_db
from temperature import schemas, utils, crud as temperature_crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_all_temperatures(
    db: Session = Depends(get_db),
        city_id: int = None,
):
    return temperature_crud.get_temperatures(
        db=db,
        city_id=city_id,
    )


@router.post("/temperatures/update/", response_model=None)
def update_temperatures(db: Session = Depends(get_db)):

    return utils.update_temperatures(db=db)
