from database import SessionLocal


def pagination_param(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}


def get_db():
    with SessionLocal() as session:
        yield session
