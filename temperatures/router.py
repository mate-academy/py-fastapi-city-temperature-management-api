from fastapi import APIRouter, HTTPException, Path, status
import temperatures.schemas as schemas
import temperatures.crud as crud
from dependencies import db_dependency

router = APIRouter(prefix="/temperature", tags=["temperature"])


@router.get("/")
def read_temperature_list(db: db_dependency, city_id: int | None = None):
    return crud.get_all_temperatures(db=db, city_id=city_id)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_city(
    db: db_dependency,
):
    return await crud.update_temperature(db=db)
