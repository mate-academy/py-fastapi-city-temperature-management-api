from fastapi import Depends, Query, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from city import crud as city_crud
from city.schemas import CityListSchema, CityRetrieveSchema, CityCreateSchema, CityUpdateSchema
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=CityListSchema)
async def city_list(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):
    total_items = await city_crud.get_total_cities_count(db)
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No cities found.")

    total_pages = (total_items + per_page - 1) // per_page
    cities = await city_crud.get_all_cities(db, skip=(page - 1) * per_page, limit=per_page)

    prev_page = f"/cities/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/cities/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return CityListSchema(
        cities=cities,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page
    )


@router.get("/cities/{city_id}", response_model=CityRetrieveSchema)
async def get_one_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    city = await city_crud.get_city_by_id(city_id=city_id, db=db)
    if not city:
        raise HTTPException(status_code=404, detail="City with the given ID was not found.")
    return CityRetrieveSchema.model_validate(city)


@router.post("/cities/", response_model=CityRetrieveSchema)
async def create_city(
        city_data: CityCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    db_city = await city_crud.get_city_by_name(db=db, city_name=city_data.name)
    if db_city:
        raise HTTPException(
            status_code=400,
            detail="City with such title is already exist."
        )

    return await city_crud.create_city(db=db, city_data=city_data)


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await city_crud.get_city_by_id(city_id=city_id, db=db)

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City with the given ID was not found."
        )

    await db.delete(city)
    await db.commit()


@router.patch("/cities/{city_id}", response_model=CityRetrieveSchema)
async def update_city(
    city_id: int,
    city_data: CityUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    city = await city_crud.get_city_by_id(db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found.")

    data_to_update = city_data.model_dump(exclude_unset=True)
    for field, value in data_to_update.items():
        setattr(city, field, value)
    await db.commit()
    await db.refresh(city)
    return CityRetrieveSchema.model_validate(city)
