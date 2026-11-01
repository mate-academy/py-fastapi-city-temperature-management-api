import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()


async def get_current_temperature(
    city_name: str,
    client: httpx.AsyncClient,
) -> float:
    key = os.getenv("WEATHER_API_KEY")

    if not key:
        raise HTTPException(
            status_code=503,
            detail="Weather API key is not configured",
        )

    try:
        response = await client.get(
            "/v1/current.json",
            params={
                "key": key,
                "q": city_name,
            },
        )
        response.raise_for_status()
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="Weather service unavailable",
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Weather service timeout",
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Failed to connect to weather service",
        )

    try:
        return float(response.json()["current"]["temp_c"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="Invalid response from weather service",
        )
