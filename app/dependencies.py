from typing import AsyncGenerator

from app.database import SessionLocal


async def get_database() -> AsyncGenerator:
	db = SessionLocal()

	try:
		yield db
	finally:
		await db.close()
