from fastapi import HTTPException
from bs4 import BeautifulSoup
import aiohttp


async def get_temperature(input_country, input_city):
    """
       API work-flow hints :

       - city name is reformatted to be recognized by the target website
       - 'aiohttp.ClientSession()' creates a client session,
       which represents a connection pool for making HTTP requests asynchronously.
       - possible responses covered
       - apparently www.timeanddate.com may not supply weather conditions for some
       states. e.g.: Lviv
       """
    input_city = input_city.replace(" ", "-")
    url = f"https://www.timeanddate.com/weather/{input_country}/{input_city}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                temperature_element = soup.find('div', class_='h2')
                if temperature_element:
                    temperature_text = temperature_element.text
                    temperature_value = temperature_text.split('\xa0')[0]
                    if temperature_element == "N/A":
                        return f"city is not supported =("

                    return f"{temperature_value}°C"
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Temperature related HTML class/tag were not found.\n"
                               f"Please inspect the HTML code.")
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Requested city and/or country were not found.\n"
                           f"Please check the input details.")
