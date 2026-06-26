from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.city import create_city
from app.crud.city import delete_city
from app.crud.city import get_cities
from app.crud.city import get_city
from app.crud.city import update_city
from app.dependencies import get_db
from app.schemas.city import CityCreate
from app.schemas.city import CityResponse

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=CityResponse)
def create(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db, city)


@router.get("", response_model=list[CityResponse])
def read_all(db: Session = Depends(get_db)):
    return get_cities(db)


@router.get("/{city_id}", response_model=CityResponse)
def read_one(city_id: int, db: Session = Depends(get_db)):
    city = get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/{city_id}", response_model=CityResponse)
def update(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    updated = update_city(db, city_id, city)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@router.delete("/{city_id}")
def delete(city_id: int, db: Session = Depends(get_db)):
    success = delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "deleted"}
