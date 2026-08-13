import pytest
import pytest_asyncio
from unittest.mock import patch
from sqlalchemy.ext.asyncio import async_sessionmaker
from testcontainers.community.postgres import PostgresContainer
from app.models import Base
from sqlalchemy.ext.asyncio import create_async_engine

@pytest.fixture(scope="session")
def start_container():
    container = PostgresContainer("postgres:16", driver=None)
    container.start()
    yield container
    container.stop()

@pytest_asyncio.fixture(scope="session")
async def test_engine(start_container):
    container = start_container
    url = container.get_connection_url()
    new_url = url.replace( "postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(new_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine


@pytest_asyncio.fixture(scope="function")
async def make_session(test_engine):
    fabric = async_sessionmaker(test_engine, expire_on_commit=False)
    async with fabric() as session:
        yield session
        await session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

@pytest_asyncio.fixture(scope="function")
async def session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)

@pytest.fixture(autouse=True)
def mock_celery_reminder():
    with patch("app.services.appointment_service.send_appointment_reminder") as mock:
        yield mock
