from fastapi import APIRouter, HTTPException

from city import crud, schemas
from dependencies import DBSessionDep, PaginationDep


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: DBSessionDep, paginate: PaginationDep):
    return crud.get_city_list(db=db, **paginate)


@router.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: DBSessionDep):
    city = crud.get_city(db=db, city_id=city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreateUpdate, db: DBSessionDep):
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(
    city_id: int, city: schemas.CityCreateUpdate, db: DBSessionDep
):
    updated_city = crud.update_city(db=db, city_id=city_id, city=city)

    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")

    return updated_city


@router.delete("/cities/{city_id}", response_model=dict)
def delete_city(city_id: int, db: DBSessionDep):
    deleted_successfully = crud.delete_city(db=db, city_id=city_id)

    if deleted_successfully:
        return {"message": "City deleted successfully"}

    raise HTTPException(status_code=404, detail="City not found")
