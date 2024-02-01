from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException, status
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
    published_date: int = Field(gt=1999, lt=2031)

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


@app.get('/books', status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found!')


@app.get('/books/published/', status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_for_published = [book for book in BOOKS if book.published_date == published_date]
    return books_for_published


@app.get('/books/', status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0, lt=6)):
    books_by_rating = [book for book in BOOKS if book.rating == rating]
    return books_by_rating


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put('/books/', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for b in range(len(BOOKS)):
        if BOOKS[b].id == book.id:
            BOOKS[b] = Book(**book.model_dump())
            book_change = True
    if not book_change:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found!')


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for item in range(len(BOOKS)):
        if BOOKS[item].id == book_id:
            BOOKS.pop(item)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found!')


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
