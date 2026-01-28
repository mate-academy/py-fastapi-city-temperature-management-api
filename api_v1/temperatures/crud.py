import asyncio
from datetime import datetime
from typing import Any
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy.orm import selectinload
from api_v1.cities import models as city_models
from api_v1.temperatures import models as temperature_models


class TemperatureCRUD:
    MAX_CONCURRENT_REQUESTS = 5  # ddos protection

    @staticmethod
    async def _fetch_current_temperature(
        client: AsyncClient, city_name: str
    ) -> tuple[datetime, float]:
        geocode_resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 1, "language": "en", "format": "json"},
        )
        geocode_resp.raise_for_status()
        geocode_data: dict[str, Any] = geocode_resp.json()
        results = geocode_data.get("results") or []
        if not results:
            raise ValueError("City not found in geocoding results")
        location = results[0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        weather_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )
        weather_resp.raise_for_status()
        weather_data: dict[str, Any] = weather_resp.json()
        current = weather_data.get("current")
        if not current or "temperature_2m" not in current or "time" not in current:
            raise ValueError("Current temperature data missing")
        return (
            datetime.fromisoformat(current["time"]),
            float(current["temperature_2m"]),
        )

    @staticmethod
    async def _build_temperature_record(
        db: AsyncSession,
        client: AsyncClient,
        semaphore: asyncio.Semaphore,
        city: city_models.City,
    ) -> temperature_models.Temperature:
        async with semaphore:
            observed_at, temperature = await TemperatureCRUD._fetch_current_temperature(
                client, city.name
            )
        record = temperature_models.Temperature(
            city_id=city.id, date_time=observed_at, temperature=temperature
        )
        record.city = city
        db.add(record)
        return record

    @staticmethod
    async def update_all_city_temperatures(
        db: AsyncSession,
    ) -> tuple[list[temperature_models.Temperature], dict[str, str]]:
        result: AsyncResult = await db.execute(select(city_models.City))
        cities = result.scalars().all()
        updated: list[temperature_models.Temperature] = []
        failed: dict[str, str] = {}
        semaphore = asyncio.Semaphore(TemperatureCRUD.MAX_CONCURRENT_REQUESTS)
        async with AsyncClient(timeout=10) as client:
            tasks = [
                TemperatureCRUD._build_temperature_record(
                    db=db, client=client, semaphore=semaphore, city=city
                )
                for city in cities
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        for city, result in zip(cities, results):
            if isinstance(result, Exception):
                failed[city.name] = str(result)
            else:
                updated.append(result)
        if updated:
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise
        return updated, failed

    @staticmethod
    async def get_all_temperatures(
        db: AsyncSession, skip: int = 0, limit: int = 100, city_id: int | None = None
    ) -> list[temperature_models.Temperature]:
        stmt = select(temperature_models.Temperature).options(
            selectinload(temperature_models.Temperature.city)
        )
        if city_id is not None:
            stmt = stmt.where(temperature_models.Temperature.city_id == city_id)
        stmt = stmt.offset(skip).limit(limit)
        result: AsyncResult = await db.execute(stmt)
        return result.scalars().all()


temperature_crud = TemperatureCRUD()
