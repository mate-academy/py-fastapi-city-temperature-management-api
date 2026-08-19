from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(  # noqa: VNE003
        Integer,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    additional_info: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    temperatures: Mapped[list['Temperature']] = relationship(
        back_populates='city',
        cascade='all, delete-orphan',
    )


class Temperature(Base):
    __tablename__ = 'temperatures'

    id: Mapped[int] = mapped_column(  # noqa: VNE003
        Integer,
        primary_key=True,
        index=True,
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey('cities.id'),
        nullable=False,
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    city: Mapped[City] = relationship(
        back_populates='temperatures',
    )
