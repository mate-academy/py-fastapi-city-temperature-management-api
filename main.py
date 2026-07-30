from typing import Annotated, Generator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import router as city_router

app = FastAPI()

app.include_router(city_router.router)

@app.get("/")
def root():
    return {"message": "Привіт, Mate Academy!"}

# python -m uvicorn main:app --reload