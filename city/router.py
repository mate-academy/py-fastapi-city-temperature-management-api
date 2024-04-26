from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from dependencies import get_db
from city import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
def read_cities(
        skip: int | None = None,
        limit: int | None = None,
        db: Session = Depends(get_db)
) -> list[schemas.CityList]:
    return crud.get_cities(db=db, skip=skip, limit=limit)


@router.post("/cities/", response_model=schemas.CityList)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db)
) -> list[schemas.CityList]:
    return crud.create_city(db=db, city=city)


@router.delete("/cities/{city.id}/", response_model=schemas.CityList)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> Response | HTTPException:
    del_city = crud.delete_city(db=db, city_id=city_id)

    if del_city is None:
        raise HTTPException(status_code=404, detail="City does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
