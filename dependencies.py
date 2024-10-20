from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
import httpx
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("Missing 'WEATHER_API_KEY'. Please check your .env file.")

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def common_city_item_params(city_id: int, db: Session = Depends(get_db)) -> dict:
    return {"db": db, "city_id": city_id}


def common_list_params(
        q: str | None,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> dict:
    return {
        "db": db,
        "q": q,
        "skip": skip,
        "limit": limit
    }


ListDep = Annotated[dict, Depends(common_list_params)]

CityItemDep = Annotated[dict, Depends(common_city_item_params)]


async def fetch_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"weather_api/{city_name}")
            response.raise_for_status()
            data = response.json()
            return data['temperature']
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching temperature: {str(e)}")

