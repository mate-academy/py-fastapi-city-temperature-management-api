from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from app.database import get_db
from app.temperatures import schemas, crud as temp_crud
from app.cities import crud as city_crud
from app.services import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update", status_code=status.HTTP_200_OK)
async def update_temperatures(db: Annotated[Session, Depends(get_db)]):
    cities = city_crud.get_cities(db)
    if not cities:
        raise HTTPException(
            status_code=400,
            detail="No cities found in database. Add cities first.",
        )

    updated_count = 0
    errors = []

    for city in cities:
        try:
            temp_value = await fetch_temperature(city.name)
            temp_crud.create_temperature(
                db, city_id=city.id, temperature=temp_value
            )
            updated_count += 1
        except Exception as e:
            errors.append(
                f"Could not update {city.name}: {str(getattr(e, 'detail', e))}"
            )

    db.commit()
    return {
        "status": "completed",
        "updated_records": updated_count,
        "failed_records": len(errors),
        "errors": errors,
    }


@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(
    db: Annotated[Session, Depends(get_db)],
    city_id: Optional[int] = Query(None),
):
    if city_id is not None:
        if not city_crud.get_city(db, city_id):
            raise HTTPException(status_code=404, detail="City not found")

    return temp_crud.get_temperatures(db, city_id=city_id)
