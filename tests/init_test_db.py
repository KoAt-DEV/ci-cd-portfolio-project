from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.base import Base
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DB_URL = os.getenv("TEST_DB_URL")

if not TEST_DB_URL:
    raise ValueError("TEST_DB_URL is not set. Please check .env or CI env.")


async def init_test_db():

    engine = create_async_engine(TEST_DB_URL, echo=False, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )

    return engine, async_session
