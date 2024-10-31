import dotenv
from fastapi import FastAPI

from city import routers as city_routers
from temperature import routers as temperature_routers


dotenv.load_dotenv()
app = FastAPI()
app.include_router(city_routers.router)
app.include_router(temperature_routers.router)
