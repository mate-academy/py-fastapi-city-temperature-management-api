from fastapi import FastAPI
from app.database import Base, engine
from app.routers import cities, temperatures

app = FastAPI()

app.include_router(cities.router)
app.include_router(temperatures.router)

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)