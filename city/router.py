from typing import Any, Annotated

from fastapi import Depends, HTTPException, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_session
from db.exc import DatabaseError
from city import schemas, crud

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.City)
async def create_city(
    data: schemas.CityCreate,
    asession: Annotated[AsyncSession, Depends(get_session)],
) -> Any:
    try:
        city = await crud.acreate_city(asession, data)
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.message)
    return city


@router.get("", response_model=list[schemas.City])
async def read_cities(
    asession: Annotated[AsyncSession, Depends(get_session)],
) -> Any:
    return list(await crud.aget_cities_list(asession))


@router.get("/{city_id}", response_model=schemas.City)
async def read_one_city(
    city_id: int,
    asession: Annotated[AsyncSession, Depends(get_session)],
) -> Any:
    city = await crud.aget_city(asession, city_id)
    if not city:
        raise HTTPException(status_code=404)
    return city


@router.put("/{city_id}", response_model=schemas.City)
async def update_one_city(
    city_id: int,
    data: schemas.CityEdit,
    asession: Annotated[AsyncSession, Depends(get_session)],
) -> Any:
    try:
        city = await crud.aupdate_city(asession, city_id, data)
    except DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.message)
    return city


@router.delete("/{city_id}")
async def delete_one_city(
    city_id: int,
    asession: Annotated[AsyncSession, Depends(get_session)],
)  -> Any:
    try:
        await crud.adelete_city(asession, city_id)
        return Response(status_code=204)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=e.message)
