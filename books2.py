from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID not required on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Author One",
                "description": "New description",
                "rating": 5
            }
        }
    }


books = [
    Book(1, "Computer Science", 'Author One', 'A very nice book!', 5),
    Book(2, "Cooking", 'Author Two', 'A very cool book!', 5),
    Book(3, "Photography", 'Author Three', 'Ok', 4),
    Book(4, "Videography", 'Author Three', 'Passable', 3),
    Book(5, "Math", 'Author One', 'Useful!', 5)
]


@app.get("/books")
async def read_all_books():
    return books


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(books) > 0:
        book.id = books[-1].id + 1
    else:
        book.id = 1

    return book

