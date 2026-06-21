from fastapi import APIRouter, HTTPException, status, Response

from dependencies import DBDep
from city import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: DBDep):
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: DBDep,
):
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_single_city(
    city_id: int,
    db: DBDep,
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_update: schemas.CityCreate,
    city_id: int,
    db: DBDep,
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city = await crud.update_city(db=db, city_id=city_id, city_update=city_update)

    return city


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    db: DBDep,
):
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    city = await crud.delete_city(db=db, city_id=city_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
