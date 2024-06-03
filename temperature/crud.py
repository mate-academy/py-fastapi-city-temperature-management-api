import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List
from sqlalchemy.orm import Session

from city.models import DBCity
from temperature.models import DBTemperature
from city.crud import get_all_cities

WEATHER_URL = "https://www.timeanddate.com/weather/"


def get_all_temperatures(db: Session) -> List[DBTemperature]:
    return db.query(DBTemperature).all()


def get_temperature_by_city_id(city_id: int, db: Session) -> DBTemperature:
    return db.query(DBTemperature).filter(
        DBTemperature.city_id == city_id
    ).first()


async def get_soup(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    async with session.get(url, ssl=False) as response:
        page = await response.text()
        return BeautifulSoup(page, "html.parser")


async def fetch_city_temperature(
        session: aiohttp.ClientSession,
        city: DBCity
) -> dict:
    city_with_temperature = {}
    try:
        soup = await get_soup(session, WEATHER_URL)
        soup_city = soup.find("a", text=city.name)
        if soup_city:
            city_temperature = soup_city.find_all_next("td", limit=3)[2].text
            text_temperature = city_temperature.split(sep=" ")[0][:2]
            city_with_temperature[city] = text_temperature
    except Exception as e:
        print(f"City not found: {city.name}, Error: {str(e)}")

    return city_with_temperature


async def get_temperatures(cities: List[DBCity]) -> dict:
    city_with_temperature = {}
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_city_temperature(session, city) for city in cities]
        results = await asyncio.gather(*tasks)
        for result in results:
            city_with_temperature.update(result)
    return city_with_temperature


async def update_all_temperatures(db: Session) -> List[DBTemperature]:
    cities = get_all_cities(db)
    city_with_temperature = await get_temperatures(cities)

    for city, temp in city_with_temperature.items():
        db_temperature = db.query(DBTemperature).filter(
            DBTemperature.city_id == city.id
        ).first()
        if db_temperature:
            db_temperature.temperature = temp

            db.commit()
            db.refresh(db_temperature)

    return db.query(DBTemperature).all()
