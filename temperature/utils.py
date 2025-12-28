import httpx


async def fetch_temperature(city_name: str) -> float:
    url = f"https://wttr.in/{city_name}?format=j1"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        return float(data["current_condition"][0]["temp_C"])

    except httpx.RequestError:
        return None
    except (KeyError, ValueError, TypeError):
        return None
