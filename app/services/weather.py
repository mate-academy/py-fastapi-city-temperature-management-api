import logging
from datetime import datetime

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

logger = logging.getLogger(__name__)


async def update_all_temperatures(db: Session) -> int:
    cities = db.scalars(select(models.City)).all()
    updated_count = 0

    async with httpx.AsyncClient(timeout=10.0) as client:
        for city in cities:
            try:
                geo_response = await client.get(
                    GEOCODING_URL,
                    params={
                        "name": city.name,
                        "count": 1
                    }
                )
                geo_response.raise_for_status()

                locations = geo_response.json().get("results", [])

                if not locations:
                    logger.warning(
                        "City not found: %s",
                        city.name
                    )
                    continue

                location = locations[0]

                weather_response = await client.get(
                    WEATHER_URL,
                    params={
                        "latitude": location["latitude"],
                        "longitude": location["longitude"],
                        "current": "temperature_2m",
                        "timezone": "UTC"
                    }
                )
                weather_response.raise_for_status()

                current = weather_response.json()["current"]

                temperature = float(current["temperature_2m"])
                recorded_at = datetime.fromisoformat(
                    current["time"]
                )

            except (
                httpx.HTTPError,
                ValueError,
                KeyError,
                TypeError
            ) as exc:
                logger.warning(
                    "Failed to fetch temperature for %s: %s",
                    city.name,
                    exc
                )
                continue

            db_temperature = models.Temperature(
                city_id=city.id,
                date_time=recorded_at,
                temperature=temperature
            )

            db.add(db_temperature)
            updated_count += 1

    if updated_count:
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

    return updated_count
