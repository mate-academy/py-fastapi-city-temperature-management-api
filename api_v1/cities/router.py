from fastapi import APIRouter, HTTPException, status
from api_v1.cities import schemas, crud
from api_v1.dependencies import DbSession, Skip, Limit


router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=list[schemas.City])
async def read_cities(db: DbSession, skip: Skip = 0, limit: Limit = 100):
    return await crud.city_crud.get_all_cities(db=db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
async def read_city(db: DbSession, city_id: int):
    city = await crud.city_crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return city


@router.post("/", response_model=schemas.City)
async def create_city(db: DbSession, city: schemas.CityCreate):
    try:
        return await crud.city_crud.create_city(db=db, city_create=city)
    except crud.CityNameConflict as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.put("/{city_id}", response_model=schemas.City)
async def update_city(db: DbSession, city_id: int, city: schemas.CityUpdate):
    try:
        updated = await crud.city_crud.update_city(
            db=db, city_id=city_id, city_update=city
        )
    except crud.CityNameConflict as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return updated


@router.patch("/{city_id}", response_model=schemas.City)
async def patch_city(db: DbSession, city_id: int, city: schemas.CityPartialUpdate):
    try:
        updated = await crud.city_crud.patch_city(
            db=db, city_id=city_id, city_patch=city
        )
    except crud.CityNameConflict as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return updated


@router.delete("/{city_id}", response_model=schemas.City | None)
async def delete_city(db: DbSession, city_id: int):
    deleted = await crud.city_crud.delete_city(db=db, city_id=city_id)
    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )
    return deleted
