from fastapi import FastAPI

from city import router as city_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


app.include_router(city_router.router)
