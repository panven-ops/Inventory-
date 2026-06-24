# ruff: noqa: E402
import sys
import os
os.environ["ENABLE_RATE_LIMIT"] = "false"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test_super_secret_key-for-ci"

from unittest.mock import AsyncMock
from redis_client import get_redis
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

#DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, "test.db")
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

engine_test = create_engine(TEST_DB_URL,connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()

#redis
def mock_redis():

    mock = AsyncMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.incr.return_value = 1
    mock.expire.return_value = True
    mock.delete.return_value = 1

    async def empty_scan(*args, **kwargs):
        return
        yield

    mock.scan_iter = empty_scan

    return mock

async def override_get_redis():

    yield mock_redis()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_redis] = override_get_redis

@pytest.fixture
def client():
    yield TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    yield
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
