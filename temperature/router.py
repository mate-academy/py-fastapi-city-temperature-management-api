from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from dependencies import get_db
from . import crud, utils

router = APIRouter()


@router.post("/temperatures/update")
def collect_temperature(db: AsyncSession = Depends(get_db)):
    asyncio.run(utils.create_temperature(db=db))
    return {
        "Message": "Temperature Updated!",
        "status_code": 204
    }


@router.get("/temperatures")
async def get_temperature(
    city_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_temperature(db=db, city_id=city_id)
