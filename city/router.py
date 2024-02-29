from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import crud, schemas
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(db: Session = Depends(get_db),
                ) -> list[schemas.City]:
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate,
                db: Session = Depends(get_db),
                ) -> schemas.City:
    return crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int,
                db: Session = Depends(get_db),
                ) -> Exception | dict[str, schemas]:
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if city:
        crud.delete_city(db=db, city_id=city_id)
        return {"message": "City deleted"}
    raise HTTPException(status_code=404, detail="City not found")


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_city(city_id: int,
              db: Session = Depends(get_db),
              ) -> schemas | Exception:
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if city:
        return city
    raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(city_id: int,
                city: schemas.CityBase,
                db: Session = Depends(get_db),
                ) -> schemas.City | Exception:
    updated_city = crud.update_city(db=db, city_id=city_id, city_data=city)
    if updated_city:
        return updated_city
    raise HTTPException(status_code=404, detail="City not found")
