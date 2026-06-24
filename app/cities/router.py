from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.cities import crud
from app.cities.schemas import CityCreate, CityResponse, CityUpdate

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityResponse,
             status_code=status.HTTP_201_CREATED)
def create_city(city: CityCreate,
                db: Session = Depends(get_db)) -> CityResponse:
    return crud.create_city(db=db, city=city)


@router.get("/", response_model=list[CityResponse])
def read_cities(db: Session = Depends(get_db)) -> list[CityResponse]:
    return crud.get_cities(db=db)


@router.get("/{city_id}", response_model=CityResponse)
def read_city(city_id: int, db: Session = Depends(get_db)) -> CityResponse:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city


@router.put("/{city_id}", response_model=CityResponse)
def update_city(
    city_id: int, city_data: CityUpdate, db: Session = Depends(get_db)
) -> CityResponse:
    db_city = crud.update_city(db=db, city_id=city_id, city_data=city_data)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return db_city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)) -> None:
    success = crud.delete_city(db=db, city_id=city_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
