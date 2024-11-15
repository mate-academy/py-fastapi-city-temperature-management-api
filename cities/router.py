from fastapi import APIRouter, Depends, HTTPException

from cities import crud, schemas

from depencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_all_cities(db=Depends(get_db)):
    return await crud.get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def get_city_by_id(city_id: int, db=Depends(get_db)):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db=Depends(get_db)):
    result = await crud.create_city(db, city)
    return result


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city_info(
        city_id: int,
        city: schemas.CityUpdate,
        db=Depends(get_db)
):
    result = await crud.update_city_info(db=db, city=city, city_id=city_id)
    if not result:
        raise HTTPException(status_code=404, detail="City not found")
    return result


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db=Depends(get_db)):
    result = await crud.delete_city(db, city_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="City does not exist or deleted already"
        )
    return result
