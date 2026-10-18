from fastapi import APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from dependencies import get_db
from temperatures import shemas, crud

router = APIRouter()



@router.get("/temperatures", response_model=list[shemas.Temperature])
async def get_temperature(db:Annotated[AsyncSession, Depends(get_db)], city_id: Annotated[int | None, Query()]) -> shemas.Temperature:

    return await crud.get_temperatures(db)


