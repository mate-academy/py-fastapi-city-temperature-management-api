from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session
from temperatures import crud

router = APIRouter()


@router.get("/temperatures/")
async def list_temperatures(
        db: AsyncSession = Depends(get_session),
        city_id: int = None
):
    """Get all temperature records."""
    temperatures = await crud.get_all_temperatures(db=db, city_id=city_id)
    return temperatures


@router.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_session)):
    """Update temperatures."""
    await crud.fetch_all_temperatures(db=db)
    return "Temperatures updated."
