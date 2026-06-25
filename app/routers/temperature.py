from fastapi import APIRouter

from app.database.config import AsyncDatabaseSession
from app.schemas.temperature import TemperatureSchema
from app.services.temperature import update_all_temperatures, list_temperatures

router = APIRouter(
    prefix="/api/temperatures",
    tags=["Temperatures API"],
)


@router.post("/update")
async def update_temperatures(db: AsyncDatabaseSession):
    count = await update_all_temperatures(db=db)
    return {"message": f"{count} Temperatures updated successfully."}


@router.get("/", response_model=list[TemperatureSchema])
async def read_temperatures(db: AsyncDatabaseSession, city_id: int = None):
    temperatures = await list_temperatures(db=db, city_id=city_id)
    return temperatures
