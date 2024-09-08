from dotenv import load_dotenv
from fastapi import FastAPI

from city import router as city
from temperature import router as temperature


load_dotenv()

app = FastAPI()

app.include_router(city.router)
app.include_router(temperature.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
