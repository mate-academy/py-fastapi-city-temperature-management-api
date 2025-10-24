from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city_CRUD import router as city_router
from temperature_api import router as temperature_router
from dependencies import get_db
from temperature_api.service import update_all_temperatures

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.post("/temperatures/update")
async def update_temperatures(session: AsyncSession = Depends(get_db)):
    await update_all_temperatures(session)
    return {"message": "Temperature update completed"}
