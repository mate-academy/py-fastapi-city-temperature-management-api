from fastapi import FastAPI

from city import router as city_router
from temperature import router as temperature_router
from pretty_response import PrettyJSONResponse

app = FastAPI()


app.include_router(
    city_router.router,
    prefix="/cities",
)

app.include_router(
    temperature_router.router,
    prefix="/temperatures",
)


@app.get("/", response_class=PrettyJSONResponse)
async def root():
    return {
        "endpoints": {
            "/cities": "Get all cities",
            "/temperatures": "Get all temperatures",
        }
    }
