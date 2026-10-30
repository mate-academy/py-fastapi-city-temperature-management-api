from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from City import schemas
from City.crud import create_new_city, city_list, city_retrieve, city_update, city_delete
from dependencies import get_db
router = APIRouter()



@router.post("/cities/", response_model=schemas.CityList)
def create(data: schemas.CityCreate, db: Session = Depends(get_db)):
    return create_new_city(db, data)


@router.get("/cities/", response_model=list[schemas.CityList])
def city_all(db: Session = Depends(get_db)):
    return city_list(db)


@router.get("/cities/{city_id}/", response_model=schemas.CityList)
def city_by_id(city_id: int, db: Session = Depends(get_db)):
    res = city_retrieve(db, city_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Unknown city!")
    return res


@router.put("/cities/{city_id}/", response_model=schemas.CityList)
def city_update_by_id(data: schemas.CityUpdate, city_id: int, db: Session = Depends(get_db)):
    res = city_update(db, city_id, data)
    if res is None:
        raise HTTPException(status_code=404, detail="Unknown city!")
    return res


@router.delete("/cities/{city_id}/", status_code=HTTP_204_NO_CONTENT)
def city_delete_by_id(city_id: int, db: Session = Depends(get_db)):
    city_delete(db, city_id)