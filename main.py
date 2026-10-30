from fastapi import FastAPI

import City.router
import Temperature.router

app = FastAPI()
app.include_router(City.router.router)
app.include_router(Temperature.router.router)