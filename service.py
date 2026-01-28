import httpx

async def fetch_temperature(city_name: str) -> float:
    url = f"https://wttr.in/{city_name}?format=%t"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10)

    return float(response.text.replace("°C", "").replace("+", ""))