from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from . import schemas, crud
from degree.crud import clear_degrees_for_city_id, clear_degrees_all

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities_list(skip: int = 0, limit: int = 10,
                          db: AsyncSession = Depends(get_db)) -> list | None:
    db_record = await crud.get_all_cities(db=db, skip=skip, limit=limit)
    if not db_record:
        raise HTTPException(
            status_code=404,
            detail="City list is empty"
        )
    return db_record


@router.get("/city/name/{city_name}", response_model=schemas.City)
async def get_cities_by_name(
        city_name: str, db: AsyncSession = Depends(get_db)
) -> schemas.City | None:
    db_record = await crud.get_city_by_name(db=db, name=city_name)
    if db_record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No city '{city_name.capitalize()}' found"
        )
    return db_record


@router.get("/cities/{city_id}", response_model=schemas.City)
@router.get("/city/id/{city_id}", response_model=schemas.City)
async def get_cities_by_id(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.City | None:
    db_record = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_record is None:
        raise HTTPException(
            status_code=404,
            detail=f"No city with id='{city_id}' found"
        )
    return db_record


@router.delete("/cities/{city_id}")
async def del_city_by_id(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> dict | None:
    db_record = await crud.delete_city(db=db, city_id=city_id)
    if not db_record:
        raise HTTPException(
            status_code=404, detail=f"Failed to delete city with id={city_id}"
        )

    # remove next line if cascade delete will work, for now it doesn't
    await clear_degrees_for_city_id(db=db, city_id=city_id)

    return db_record


@router.delete("/cities/",
               description=" Carefully! Deletes ALL Cities!")
async def del_city(db: AsyncSession = Depends(get_db)) -> dict | None:
    db_record = await crud.delete_all_cities(db=db)
    if not db_record:
        raise HTTPException(status_code=404,
                            detail="Failed to execute deletion")

    # remove next line if cascade delete will work, for now it doesn't
    await clear_degrees_all(db=db)

    return db_record


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate,
                      db: AsyncSession = Depends(get_db)
                      ) -> dict | Exception:
    db_record = await crud.get_city_by_name(db=db, name=city.name)
    if db_record is not None:
        raise HTTPException(
            status_code=403,
            detail=f"City '{city.name.capitalize()}' already exists"
        )
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.CityBase)
async def city_mod(
        city_id: int, city: schemas.CityBase,
        db: AsyncSession = Depends(get_db)
) -> dict | Exception:
    db_record = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_record is None:
        raise HTTPException(
            status_code=420,
            detail=f"City with id={city_id} not found"
        )
    db_record = await crud.get_city_by_name_exclude_id(
        db=db, city_name=city.name, city_id=city_id
    )
    if db_record is not None:
        raise HTTPException(
            status_code=403,
            detail=f"City '{city.name.capitalize()}' already exists"
        )
    return await crud.update_city_info(db=db, city=city, city_id=city_id)
