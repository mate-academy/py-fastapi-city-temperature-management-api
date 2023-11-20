from fastapi import FastAPI

from city import router as cite_router
from temperature import router as temperature_router

app = FastAPI()
app.include_router(cite_router.router)
app.include_router(temperature_router.router)


@app.get("/")
async def root():
    return {"Message": "main page"}
