from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from Temperature import schemas, crud
from database import get_db

app = FastAPI()

@app.get("/temperatures/", response_model=List[schemas.Temperature])
async def get_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int = None
):
    return await crud.get_temperatures(db=db, city_id=city_id)
