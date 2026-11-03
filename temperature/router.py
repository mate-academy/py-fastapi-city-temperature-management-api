import httpx
from fastapi import APIRouter, HTTPException

from dependecies import DbSession
from temperature import schemas, crud

router = APIRouter()

@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_temperatures(
        db: DbSession,
        city_id: int | None = None
):
    return await crud.get_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperatures(db: DbSession):
    try:
        return await crud.update_temperatures(db=db)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=400,
            detail="Bad Request"
        )
