from dependencies import app


@app.get("/")
def root() -> dict:
    return {"message": "Initialized "}
