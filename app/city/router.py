from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.city import schemas, crud
from app.city.models import DBCity
from app.dependencies import get_session

router = APIRouter(tags=["Cities"])


@router.get("/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_session)) -> [DBCity]:
    return await crud.get_all_city(db=db)


@router.get("/{city_id}/", response_model=schemas.City)
async def read_city(
        id: int,
        db: AsyncSession = Depends(get_session)
) -> DBCity:
    return await crud.get_city(city_id=id, db=db)


@router.post("/", response_model=schemas.CityCreate)
async def add_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_session)
) -> DBCity:
    result = await crud.get_city_by_name(db=db, name_city=city.city)
    if result:
        raise HTTPException(
            status_code=400, detail="Such city for City already exist"
        )

    city = await crud.create_city(db=db, city=city)
    await db.commit()
    return city


@router.put("/{city_id}/update/", response_model=schemas.CityUpdate)
async def update_city(
    id: int, city: schemas.CityUpdate, db: AsyncSession = Depends(get_session)
) -> DBCity:
    city = await crud.update_city(
        city_id=id,
        new_city=city.city,
        additional_info=city.additional_info,
        db=db,
    )
    return city


@router.delete("/{city_id}/", response_model=schemas.City)
async def delete_city(
        id: int,
        db: AsyncSession = Depends(get_session)
) -> DBCity:
    result = await crud.delete_city(city_id=id, db=db)
    return result
