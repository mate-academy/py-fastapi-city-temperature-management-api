from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "main page"}
