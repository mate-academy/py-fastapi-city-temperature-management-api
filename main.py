from fastapi import FastAPI

from database import Base, engine
from temperature_management.router import router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello world!"}
