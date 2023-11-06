from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temperature import crud, models, schemas
from database import engine
from dependencies import get_db
from pretty_response import PrettyJSONResponse

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/update/", response_class=PrettyJSONResponse)
def create_update_temperatures(db: Session = Depends(get_db)):
    crud.create_update_temperatures(db)
    return {"message": "Fetching temperatures initiated, please wait a few minutes."}


@router.get("/", response_model=schemas.TemperatureRead, response_class=PrettyJSONResponse)
def read_temperatures(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        city_id: int = None
):
    temperatures = crud.get_temperatures(
        db=db, skip=skip, limit=limit, city_id=city_id
    )
    return temperatures

