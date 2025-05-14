from typing import List
import logging

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import insert, update

import models


def get_logger(name: str) -> logging.Logger:
    """Return a logger object with custom settings."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = get_logger(__name__)


def create_city_temperature_records(
        city_temperature_data: List[dict]
) -> List[dict]:
    """Creates a list of temperature records for cities."""

    return [
        {
            "city_id": city_id,
            "temperature": temperature,
        }
        for city_id, temperature
        in city_temperature_data.items()
    ]


async def insert_new_temperature_records(
        db: AsyncSession,
        new_records: List[dict]
) -> str:
    """
    Inserts new temperature records for cities into the database.

    :param db: an active database session
    :param new_records: a list of dicts with keys "city_id" and "temperature"
    :return: a success message if the new records were inserted,
             otherwise an error message
    """
    insert_query = insert(models.Temperature).returning(models.Temperature)
    try:
        await db.execute(insert_query, new_records)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Error inserting temperatures: {e}")
        return "Failed to insert temperature records."

    return f"New temperatures records for {new_records} created."


async def update_existing_temperature_records(
        db: AsyncSession,
        existing_records: List[dict]
) -> str:
    """
    Updates existing temperature records for cities in the database.

    :param db: an active database session
    :param existing_records: a list of dicts with keys "city_id", "temperature"
    :return: a success message if the existing records were updated,
             otherwise an error message
    """
    try:
        await db.execute(update(models.Temperature), existing_records)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating temperatures: {e}")
        return "Failed to update temperature records."

    return f"Updated existing temperature records for {existing_records}."
