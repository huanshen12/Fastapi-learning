from fastapi import FastAPI

app = FastAPI()
@app.middleware("http")
async def middleware1(request,call_next):
    print("中间件1 开始")
    response = await call_next(request)
    print("中间件1 结束")
    return response
@app.middleware("http")
async def middleware2(request,call_next):
    print("中间件2 开始")
    response = await call_next(request)
    print("中间件2 结束")
    return response
