from fastapi import FastAPI

from city import router as cite_router

app = FastAPI()
app.include_router(cite_router.router)


@app.get("/")
async def root():
    return {"Message": "main page"}
