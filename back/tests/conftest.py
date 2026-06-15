import sys
import os
os.environ["ENABLE_RATE_LIMIT"] = "false"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from unittest.mock import MagicMock
import redis_client
redis_client.redis_client = MagicMock()
redis_client.redis_client.get.return_value = None
redis_client.redis_client.scan_iter.return_value = []

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from slowapi import Limiter
from slowapi.util import get_remote_address
import lim

# Disable rate limiting για tests
lim.limiter = Limiter(key_func=get_remote_address, enabled=False)

# Absolute path για το test.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DB_PATH = os.path.join(BASE_DIR, "test.db")
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

engine_test = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    yield TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    yield
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
