from city import crud
from city.schemas import CityBase, City, CityCreate, CityUpdate, CityDelete
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db

router = APIRouter(prefix="/city", tags=["City"])


@router.get("/", response_model=list[City])
def get_all_city(db: Session = Depends(get_db)):
    return crud.get_all_city(db=db)


@router.get("/{city_id}")
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    return crud.get_city_by_id(db=db, city_id=city_id)


@router.post("/create/", response_model=CityCreate)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    get_or_not = crud.get_city_by_name(db=db, name=city.name)

    if get_or_not:
        raise HTTPException(
            status_code=400,
            detail="This name already exist"
        )

    return crud.create_city(db=db, city=city)


@router.put("/update/{city_id}", response_model=CityUpdate)
def update_city(city_id: int,
                new_city: CityUpdate,
                db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    update_city = crud.update_city(db, city_id, new_city)
    return update_city


@router.delete("/delete/{city_id}", response_model=CityDelete)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    deleted_city = crud.delete_city(db=db, city_id=city_id)
    return deleted_city
