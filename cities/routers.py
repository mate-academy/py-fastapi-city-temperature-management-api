from fastapi import APIRouter, Depends, HTTPException

from cities import schemas, crud

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

city_router = APIRouter()


@city_router.get("/cities/", response_model=list[schemas.CitySchema])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@city_router.post("/cities/", response_model=schemas.CitySchema)
async def create_city(
    city: schemas.CityCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@city_router.get("/cities/{city_id}/", response_model=schemas.CitySchema)
async def read_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_city_by_id(city_id=city_id, db=db)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="City with current id none exist"
        )

    return result


@city_router.put("/cities/{city_id}/", response_model=schemas.CitySchema)
async def update_city(
        city_id: int,
        city: schemas.CityUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await crud.update_city(db=db, city_id=city_id, city=city)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="City with the given id does not exist"
        )

    return result


@city_router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_city(db=db, city_id=city_id)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="City with current id none exist"
        )

    return result