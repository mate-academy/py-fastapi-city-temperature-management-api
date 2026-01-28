from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_session import get_db
import schemas.city as schemas
import crud.city as crud

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

@router.post("/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city_data=city)

@router.get("/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)

@router.get("/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db, city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return None
