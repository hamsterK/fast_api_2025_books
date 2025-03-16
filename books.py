from fastapi import FastAPI, Body

app = FastAPI()

books = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt, David Thomas", "year": 1999, "category": "science"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "category": "science"},
    {"id": 3, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "year": 2017, "category": "science"},
    {"id": 4, "title": "You Don’t Know JS", "author": "Kyle Simpson", "year": 2014, "category": "js"},
    {"id": 5, "title": "Python Crash Course", "author": "Eric Matthes", "year": 2015, "category": "python"}
]


@app.get("/")
async def first_api():
    return {"message": "Hello!"}


@app.get("/books")
async def read_all_books():
    return books


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in books:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/by_author/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    books.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(books)):
        if books[i].get('title').casefold() == updated_book.get('title').casefold():
            books[i] = updated_book


@app.delete("/books/delete_book")
async def delete_book(book_title: str):
    for i in range(len(books)):
        if books[i].get('title').casefold() == book_title.casefold():
            books.pop(i)
            break

# uvicorn books:app --reload
