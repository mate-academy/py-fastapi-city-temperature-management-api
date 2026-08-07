# async def weather(city_name: str) -> float:
#     async with ClientSession() as session:
#         latitude = 0
#         longitude = 0
#         temperature = 0
#         async with session.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={settings.OPENWEATHER_API_KEY}") as response:
#             response = await response.json()
#             latitude = response[0]["lat"]
#             longitude = response[0]["lon"]
#         async with session.get(
#             f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
#         ) as response:
#             response = await response.json()
#             temperature = response["main"]["temp"]
#     return temperature
#
# async def get_weather(citi_name: str) -> float:
#     return await weather(citi_name)
#
#
# TemperatureDependency = Annotated[float, Depends(get_weather)]
