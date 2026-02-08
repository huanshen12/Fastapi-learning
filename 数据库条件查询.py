from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost/fastapiproject?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,            #打印日志
    pool_size=10,           #连接池
    max_overflow=20         #额外的连接池
)

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now(),comment="更新时间")

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True,comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255),comment="书籍名称")
    author: Mapped[str] = mapped_column(String(255),comment="作者")
    price: Mapped[float] = mapped_column(Float,comment="价格")
    publisher: Mapped[str] = mapped_column(String(255),comment="出版社")

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(apps: FastAPI):
    await create_table()
    yield
    await async_engine.dispose()
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@app.get("/book/books")
async def get_books(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(select(Book))
    # book = result.scalars().all()
    # book = result.scalars().first()
    book = await db.get(Book,1)
    return book

@app.get("/book/book_id/{book_id}")
async def get_book(book_id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    return book

@app.get("/book/book_price")
async def get_book_price(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.price >= 40))
    book = result.scalars().all()
    return book

@app.get("/book/search")
async def search_book(db: AsyncSession = Depends(get_db)):
    # result = await db.execute(select(Book).where(Book.author.like("曹%")))
    # result = await db.execute(select(Book).where(Book.author.like("曹%")))
    # result = await db.execute(select(Book).where((Book.author.like("曹%")) & (Book.price < 10)))
    # result = await db.execute(select(Book).where((Book.author.like("曹%")) | (Book.price < 10)))
    id_list = [1,3,6]
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))

    book = result.scalars().all()
    return book
