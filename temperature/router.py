from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
        city_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def update_temperatures_task(db: Session = Depends(get_db)):
    await crud.update_temperatures(db)
    return {"message": "Temperatures updated successfully"}
