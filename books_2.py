from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

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
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2029
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get('/books')
async def get_all_books():
    return BOOKS


@app.get('/books/{book_id}')
async def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None


@app.get('/books/published/')
async def get_books_by_published_date(published_date: int):
    books_for_published = [book for book in BOOKS if book.published_date == published_date]
    return books_for_published


@app.get('/books/')
async def get_books_by_rating(rating: int):
    books_by_rating = [book for book in BOOKS if book.rating == rating]
    return books_by_rating


@app.post('/books')
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put('/books/')
async def update_book(book: BookRequest):
    for b in range(len(BOOKS)):
        if BOOKS[b].id == book.id:
            BOOKS[b] = Book(**book.model_dump())


@app.delete('/books/{book_id}')
async def delete_book(book_id: int):
    for item in range(len(BOOKS)):
        if BOOKS[item].id == book_id:
            BOOKS.pop(item)
            break


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
