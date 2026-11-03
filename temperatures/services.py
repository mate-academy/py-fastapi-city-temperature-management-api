import os
import httpx


async def get_temp(city: str) -> float:
    url = f"http://api.weatherapi.com/v1/current.json?key=be544d21038b4fd499b162423261610&q={city}"
    # url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={city}"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        return res.json()["current"]["temp_c"]
