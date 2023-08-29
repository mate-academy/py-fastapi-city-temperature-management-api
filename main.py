from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"message": "Welcome to the main paige"}
