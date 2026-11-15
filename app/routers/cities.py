from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from app import crud, schemas
from app.dependencies import CityDep, DbSession

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post(
    "",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
def create_city(city_in: schemas.CityCreate, db: DbSession) -> schemas.City:
    existing = crud.get_city_by_name(db, city_in.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city_in.name}' already exists",
        )
    try:
        return crud.create_city(db, city_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city_in.name}' already exists",
        ) from None


@router.get("", response_model=list[schemas.City])
def list_cities(db: DbSession) -> list[schemas.City]:
    return crud.get_cities(db)


@router.get("/{city_id}", response_model=schemas.City)
def get_city(city: CityDep) -> schemas.City:
    return city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(
    city: CityDep,
    city_in: schemas.CityUpdate,
    db: DbSession,
) -> schemas.City:
    if city_in.name is not None:
        existing = crud.get_city_by_name(db, city_in.name)
        if existing is not None and existing.id != city.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"City with name '{city_in.name}' already exists",
            )
    try:
        return crud.update_city(db, city, city_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"City with name '{city_in.name}' already exists",
        ) from None


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city: CityDep, db: DbSession) -> Response:
    crud.delete_city(db, city)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
