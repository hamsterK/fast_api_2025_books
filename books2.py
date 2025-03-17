from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID not required on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(ge=1900, le=datetime.today().year + 5, )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Author One",
                "description": "New description",
                "rating": 5,
                "published_date": 2020
            }
        }
    }


books = [
    Book(1, "Computer Science", 'Author One', 'A very nice book!', 5, 2020),
    Book(2, "Cooking", 'Author Two', 'A very cool book!', 5, 2021),
    Book(3, "Photography", 'Author Three', 'Ok', 4, 1999),
    Book(4, "Videography", 'Author Three', 'Passable', 3, 2015),
    Book(5, "Math", 'Author One', 'Useful!', 5, 2017)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in books:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(ge=1900, le=datetime.today().year+5)):
    books_to_return = []
    for book in books:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book
            return
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")
