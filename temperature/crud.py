import json

import asyncio

import urllib.parse
import urllib.request

from typing import Any, Sequence

from sqlalchemy import select

from temperature import models

from sqlalchemy.orm import Session

from temperature.models import Temperature


async def fetch_json(url: str, timeout: float = 15.0) -> dict[str, Any]:
    """
    Async wrapper around stdlib urllib to avoid adding new dependencies.
    Runs the blocking HTTP call in a thread.
    """

    def _blocking_fetch() -> dict[str, Any]:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "py-fastapi-city-temperature-management-api/1.0",
                "Accept": "application/json",
            },
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
        return json.loads(data)

    return await asyncio.to_thread(_blocking_fetch)


async def fetch_current_temperature_celsius(city_name: str) -> float:
    """
    Uses Open-Meteo Geocoding API to get lat/lon, then Open-Meteo Forecast API
    to get the current temperature (°C).
    """
    q = urllib.parse.quote(city_name)

    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={q}&count=1&language=en&format=json"
    geo = await fetch_json(geocode_url)

    results = geo.get("results") or []
    if not results:
        raise ValueError(f"City not found in geocoding API: {city_name}")

    lat = results[0]["latitude"]
    lon = results[0]["longitude"]

    weather_url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current=temperature_2m"
    )
    weather = await fetch_json(weather_url)

    current = weather.get("current") or {}
    temp = current.get("temperature_2m")
    if temp is None:
        raise ValueError(f"No current temperature returned for city: {city_name}")

    return float(temp)


def get_temperatures(
    db: Session,
    *,
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Temperature]:
    stmt = select(models.Temperature).order_by(models.Temperature.date_time.desc())
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)

    return db.scalars(stmt.offset(skip).limit(limit)).all()
