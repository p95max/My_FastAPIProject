from fastapi import FastAPI, Depends
from pydantic import BaseModel
from database import get_db
from models import Book

app = FastAPI()

class BookSchema(BaseModel):
    id: int
    title: str
    author: str | None

@app.get("/book/{id}")
def get_book(id: int, db=Depends(get_db)):
    return db.query(Book).get(id)


@app.post("/add_book")
def add_book(book: BookSchema, db=Depends(get_db)):
    db.add(Book(**book.model_dump()))
    db.commit()


@app.delete("/book/{id}")
def delete_book(id: int, db=Depends(get_db)):
    db.query(Book).filter_by(id=id).delete()
    db.commit()


@app.get("/all_books")
def get_all_books(db=Depends(get_db)):
    return db.query(Book).all()
