from fastapi import FastAPI, Body

from schemas import Book

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]



@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{item_book}")
async def get_one_book(item_book: str):
    book = [b for b in BOOKS if b.get("title").casefold() == item_book.casefold()]
    return book


@app.get("/books/{book_author}")
async def read_category_by_query(book_author: str, category: str):
    book = [
        b for b in BOOKS if b.get("author").casefold() == book_author.casefold() and
                            b.get("category").casefold() == category.casefold()
    ]
    return book


@app.post("/books/create_book")
async def create_book(new_book: Book):
    return BOOKS.append(new_book.model_dump())


@app.put("/books")
async def update_book(book: Book):
    for item in range(len(BOOKS)):
        if BOOKS[item].get("title").casefold() == book.title.casefold():
            BOOKS[item] = book.model_dump()


@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for item in range(len(BOOKS)):
        if BOOKS[item].get("title").casefold() == book_title.casefold():
            BOOKS.pop(item)
            break
