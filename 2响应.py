from fastapi import FastAPI
from fastapi.responses import  HTMLResponse,FileResponse
from pydantic import BaseModel

app = FastAPI()

class News(BaseModel):
    id :int
    title :str
    content :str
@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/html",response_class=HTMLResponse)
async def html():
    return "<h1>这是一级标题</h1>"

@app.get("/file")
async def get_file():
    path ="./file/1.png"
    return FileResponse(path)

@app.get("/news/{id}")
async def get_news(id:int):
    return {
        "id":id,
        "title":"新闻标题",
        "content":"新闻内容"
          }
