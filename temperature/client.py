from httpx import AsyncClient

from city import models


async def fetch_temperature_data(
    city: models.City, api_url: str, api_key: str, client: AsyncClient
) -> dict:
    response = await client.get(api_url, params={"key": api_key, "q": city.name})
    response.raise_for_status()
    json_data = response.json()
    extracted_data = {
        "temperature": json_data["current"]["temp_c"],
        "date_time": json_data["current"]["last_updated"],
    }
    return extracted_data
