from fastapi import FastAPI, Path,Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/book/{id}")
async def get_id(id: int):
    return {f"这是第{id}本书"}

@app.get("/news_id/{id}")
async def news_id(id:int = Path(...,gt = 0,lt = 101,description="新闻编号，取1-100")):
    return {"msg":f"这是第{id}条新闻"}

@app.get("/news_type/{type}")
async def news_type(type:str = Path(...,min_length = 1,max_length = 10,description="新闻类型")):
    return {"msg":f"这是{type}类型的新闻"}

@app.get("/books")
async def get_books(
        type:str = Query("python开发",min_length = 1,max_length = 10,description="图书类型"),
        price:int = Query(...,gt = 49,lt = 101,description="图书价格")
):
    return {"msg":f"这是{type}类型的图书，价格是{price}"}
