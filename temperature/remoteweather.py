import httpx

async def get_current_temperature(city_name: str) -> float | None:
    async with httpx.AsyncClient(timeout=10.0) as client:

        url = f"https://wttr.in/{city_name}?format=j1"

        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            temperature = float(data["current_condition"][0]["temp_C"])
            return temperature
        except httpx.HTTPStatusError as e:
            print(f"Weather service returned HTTP {e.response.status_code} for city '{city_name}'.")
            return None
        except httpx.RequestError as e:
            print(f"Failed to connect to weather service for city '{city_name}': {e}")
            return None
        except (KeyError, IndexError, ValueError, TypeError) as e:
            print(f"Unexpected weather data format for city '{city_name}': {e}")
            return None