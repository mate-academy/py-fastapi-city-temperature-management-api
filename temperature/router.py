import httpx
from fastapi import APIRouter, HTTPException

from dependencies import DbSession
from temperature import crud, schemas

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.get("", response_model=list[schemas.Temperature])
async def temperatures_get(db: DbSession, city_id: int | None = None):
    return await crud.get_temperatures(db=db, city_id=city_id)


@router.post("/update", response_model=list[schemas.Temperature])
async def temperatures_update(db: DbSession):
    try:
        return await crud.update_temperatures(db=db)
    except httpx.HTTPError:
        raise HTTPException(status_code=400, detail="Bad Request")
