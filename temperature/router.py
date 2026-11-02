from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from temperature import crud, schemas

router = APIRouter()


@router.post("/temperatures/update/", status_code=201)
async def update_temperatures(db: Session = Depends(get_db)):
    await crud.update_temperatures(db)
    return {"message": "Temperatures updated"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_temperatures(
        db, city_id=city_id, skip=skip, limit=limit
    )
