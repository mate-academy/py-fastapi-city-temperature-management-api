from fastapi import APIRouter, HTTPException, Path, status
import cities.schemas as schemas
from dependencies import db_dependency
import cities.crud as crud


router = APIRouter(prefix="/cities", tags=["city"])


@router.get("/", response_model=list[schemas.City], status_code=status.HTTP_200_OK)
def read_city_list(db: db_dependency):
    return crud.get_all_cities(db=db)


@router.get("/{city_id}", response_model=schemas.City, status_code=status.HTTP_200_OK)
def read_city(db: db_dependency, city_id: int = Path(gt=0)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/", response_model=schemas.CityBase, status_code=status.HTTP_201_CREATED)
def read_city(db: db_dependency, city: schemas.CityBase):
    return crud.create_city(db=db, city=city)


@router.put("/{city_id}", response_model=schemas.CityBase)
def update_city(
    db: db_dependency,
    city: schemas.CityBase,
    city_id: int = Path(gt=0),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.update_city_by_id(db=db, city_id=city_id, city=city)


@router.delete("/{city_id}")
def delete_city(
    db: db_dependency,
    city_id: int = Path(gt=0),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.delete_city_by_id(db=db, city_id=city_id)
