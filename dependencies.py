from database import SessionLocal


async def pagination_param(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}


async def get_db():
    async with SessionLocal() as session:
        yield session
