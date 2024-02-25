import aiohttp

KEY = "efab8efa7c2c4f828f4101225242502"


async def get_weather(city: str) -> int | None:
    async with aiohttp.ClientSession() as session:
        url = f"https://api.weatherapi.com/v1/current.json?KEY={KEY}&q={city}"
        async with session.get(url) as resp:
            if resp.status == 200:
                temp_city = await resp.json()
                return temp_city["current"]["temp_c"]
