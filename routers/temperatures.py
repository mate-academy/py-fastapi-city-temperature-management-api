from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, services
from ..database import get_db
from datetime import datetime

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    results = await services.update_all_temperatures(db)
    success = sum(1 for r in results if r["status"] == "success")
    return {
        "message": f"Updated temperatures for {success}/{len(results)} cities",
        "details": results
    }


@router.get("/", response_model=list[schemas.Temperature])
def read_temperatures(
        city_id: int = Query(None, description="Filter by city ID"),
        start_date: datetime = Query(None, description="Filter by start date"),
        end_date: datetime = Query(None, description="Filter by end date"),
        db: Session = Depends(get_db)
):
    temps = crud.get_temperatures(db, city_id)

    # Apply date filtering
    if start_date:
        temps = [t for t in temps if t.date_time >= start_date]
    if end_date:
        temps = [t for t in temps if t.date_time <= end_date]

    return temps