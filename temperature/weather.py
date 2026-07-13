import httpx

API_KEY = "46527bf17d37498abfc91729260307"


async def get_temperature(city_name: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.weatherapi.com/v1/current.json",
            params={
                "key": API_KEY,
                "q": city_name,
            },
        )

    response.raise_for_status()

    data = response.json()

    return data["current"]["temp_c"]

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(get_temperature("Kyiv")))