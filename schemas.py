from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookList(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Book(BookBase):
    id: int
    author: "Author"
    model_config = ConfigDict(from_attributes=True)


class Author(AuthorBase):
    id: int
    books: list[BookList]

    model_config = ConfigDict(from_attributes=True)
