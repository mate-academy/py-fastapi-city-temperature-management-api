from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from contextlib import asynccontextmanager

import crud
import schemas
import models
from database import engine, get_db
from temperature_service import update_all_temperatures


# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Weather & City API",
    description="API for managing cities and their temperature measurements",
    version="1.0.0",
    lifespan=lifespan,
)

# ==================== CITY ENDPOINTS ====================


@app.post("/cities", response_model=schemas.City, status_code=201)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    """
    Создать новый город.
    """
    # Check if city with same name exists
    existing = await crud.get_city_by_name(db, city.name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"City with name '{city.name}' already exists"
        )

    return await crud.create_city(db, city)


@app.get("/cities", response_model=List[schemas.City])
async def get_cities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """
    Получить список всех городов с пагинацией.
    """
    return await crud.get_cities(db, skip=skip, limit=limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить подробную информацию о конкретном городе.
    """
    city = await crud.get_city(db, city_id)
    if not city:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить данные конкретного города.
    """
    # Check if updating name and if it conflicts
    if city_update.name:
        existing = await crud.get_city_by_name(db, city_update.name)
        if existing and existing.id != city_id:
            raise HTTPException(
                status_code=400,
                detail=f"City with name '{city_update.name}' already exists",
            )

    updated = await crud.update_city(db, city_id, city_update)
    if not updated:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return updated


@app.delete("/cities/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить конкретный город
    (каскадное удаление всех его температурных записей).
    """
    deleted = await crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )
    return None


# ==================== TEMPERATURE ENDPOINTS ====================


@app.post(
    "/temperatures/update",
    response_model=schemas.TemperatureUpdateResponse
)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    """
    Получить текущую температуру для всех городов в базе данных из внешнего API
    и сохранить эти данные в таблице Temperature.
    """
    result = await update_all_temperatures(db)
    return result


@app.get("/temperatures", response_model=List[schemas.TemperatureWithCity])
async def get_temperatures(
    city_id: Optional[int] = Query(None, description="Filter by city ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """
    Получить список всех записей о температуре.
    Можно отфильтровать по city_id.
    """
    temps = await crud.get_temperatures_with_cities(db, city_id=city_id)

    # Convert to response schema with city name
    result = []
    for temp in temps:
        result.append(
            schemas.TemperatureWithCity(
                id=temp.id,
                city_id=temp.city_id,
                temperature=temp.temperature,
                date_time=temp.date_time,
                city_name=temp.city.name if temp.city else "Unknown",
            )
        )

    # Apply pagination manually (since we need joined load)
    return result[skip: skip + limit]


@app.get("/temperatures/stats/{city_id}")
async def get_city_temperature_stats(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику по температуре для конкретного города.
    """
    city = await crud.get_city(db, city_id)
    if not city:
        raise HTTPException(
            status_code=404, detail=f"City with id {city_id} not found"
        )

    temps = await crud.get_temperatures(db, city_id=city_id)
    if not temps:
        return {
            "city_id": city_id,
            "city_name": city.name,
            "message": "No temperature data available",
        }

    temperatures = [t.temperature for t in temps]
    return {
        "city_id": city_id,
        "city_name": city.name,
        "total_measurements": len(temperatures),
        "average_temperature": round(sum(temperatures) / len(temperatures), 2),
        "min_temperature": min(temperatures),
        "max_temperature": max(temperatures),
        "last_measurement": temps[0].date_time if temps else None,
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Weather & City API is running"}
