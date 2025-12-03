from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from City import schemas
from City import crud
from database import get_db

app = FastAPI()



@app.get("/cities/", response_model=List[schemas.City])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)

@app.post("/cities/", response_model=schemas.City)
async def create_city(
        city_data: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db=db, city=city_data)

@app.post("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_city(db=db, id=city_id)
