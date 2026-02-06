from fastapi import FastAPI, Depends, Query

app = FastAPI()

async def news_list(
        page:int = Query(1,ge = 1),
        limit:int = Query(10,ge = 1,le = 100)
):
    return {"page":page,"limit":limit}
@app.get("/news")
async def get_news(common = Depends(news_list)):
    return common
