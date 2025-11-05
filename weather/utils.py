import httpx
import asyncio


async def get_temperature_for_cities(city_names: list):
    result = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for city in city_names: 
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=1246b774fd2f962fd0e949571739b753&units=metric"
            tasks.append(client.get(url))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            data = response.json()
            if data.get("cod") == 200:
                result.append((data["name"], data["main"]["temp"]))
            else:
                result.append((None, None))
    return result
