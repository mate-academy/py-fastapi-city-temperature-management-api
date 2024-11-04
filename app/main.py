from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.database import Base, engine
from app.routers import cities, temperatures

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(cities.router, prefix="/cities")
app.include_router(temperatures.router, prefix="/temperatures")

@app.middleware("http")
async def add_exception_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
