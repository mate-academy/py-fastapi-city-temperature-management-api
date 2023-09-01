import uvicorn

from fastapi import FastAPI
from cities import router as city_router
from temperature import router as temperature_router
app = FastAPI()


@app.get("/")
async def hello() -> dict:
    return {"greetings": "Hello world"}

api_version_prefix = "/api/v1"

app.include_router(
    city_router.router,
    prefix=f"{api_version_prefix}/cities",
    tags=["cities"]
)
app.include_router(
    temperature_router.router,
    prefix=f"{api_version_prefix}/temperatures",
    tags=["temperatures"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
