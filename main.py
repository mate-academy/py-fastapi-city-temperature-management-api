from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from cities import router as city_router
from temperatures import router as temperature_router

app = FastAPI()

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
def root():
    return RedirectResponse(url="/cities")
