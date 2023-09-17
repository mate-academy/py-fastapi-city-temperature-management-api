from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temperature import schemas, crud, models
from dependencies import get_db

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def list_temperatures(
    city_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    queryset = db.query(models.Temperature)
    if city_id is not None:
        queryset = queryset.filter(models.Temperature.city_id == city_id)

    return queryset.offset(skip).limit(limit).all()
