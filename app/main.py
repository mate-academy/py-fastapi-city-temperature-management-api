from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI(
    title="City & Temperature Management API",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}
