from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities", response_model=list[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_list_of_cities(db=db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city_by_id(
        city_id: int, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_by_id(
        city_id: int,
        additional_info: str,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.update_city(
        db=db,
        city_id=city_id,
        additional_info=additional_info
    )
    return db_city


@router.delete("/cities/{city_id}", response_model=None)
async def delete_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db),
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    city_name = db_city.name

    await crud.delete_city_by_id(db=db, city_id=city_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": f"City {city_name} with id: {city_id} was deleted"}
    )
