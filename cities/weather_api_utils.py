import main


async def get_weather(city_name: str):
    response = await main.get_http_client().get(
        f"{main.WEATHER_API_URL}"
        f"?key={main.WEATHER_API_KEY}&q={city_name}&aqi=no"
    )
    if response.status_code == 200:
        json = response.json()
        return json.get("current").get("temp_c")
