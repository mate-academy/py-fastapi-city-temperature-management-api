import os

from datetime import datetime

from typing import Optional, List, AsyncGenerator

from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


engine = create_engine("sqlite:///api_city_tempr.db")

async_engine = create_async_engine("sqlite+aiosqlite:///./api_city_tempr.db")

async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class BaseModel(DeclarativeBase):
    pass


class DBCity(BaseModel):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True)
    additional_info: Mapped[Optional[str]] = mapped_column(String(255))

    temperatures: Mapped[List["DBTemperature"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )


class DBTemperature(BaseModel):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id"),
        index=True,
    )
    date_time: Mapped[datetime]
    temperature: Mapped[float]

    city: Mapped["DBCity"] = relationship(back_populates="temperatures")


def create_db():
    return BaseModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


if not os.path.isfile("./api_city_tempr.db"):
    print("Creating api_city_tempr.db")
    create_db()
