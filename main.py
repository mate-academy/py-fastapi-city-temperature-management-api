from fastapi import FastAPI
from city import routers as city_router
app = FastAPI()

app.include_router(city_router.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
