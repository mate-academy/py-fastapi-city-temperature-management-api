from fastapi import FastAPI

import city.router
import temperature.router

app = FastAPI()

app.include_router(city.router.router)
app.include_router(temperature.router.router)
