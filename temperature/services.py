import httpx


async def fetch_temperature(city_name: str) -> float:
    url = f"https://wttr.in/{city_name}?format=j1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()
    return float(data["current_condition"][0]["temp_C"])
