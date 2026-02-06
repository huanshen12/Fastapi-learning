from fastapi import FastAPI
from pydantic import BaseModel,Field


class Book(BaseModel):
    bookname: str = Field(...,max_length=20,min_length=2)
    author: str = Field(min_length=2,max_length=10)
    publisher: str = Field(default="河北出版社")
    price: float = Field(...,gt=0)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/book")
async def book(book:Book):
    return book
