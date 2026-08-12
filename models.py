from datetime import date

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(511), nullable=False)
    books: Mapped[list["DBBook"]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(511), nullable=False)
    publication_date: Mapped[date] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["DBAuthor"] = relationship(back_populates="books")
