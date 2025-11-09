# backend/tests/test_history.py
import pytest
from httpx import AsyncClient
from app.main import app
from app.core.db import Base, engine, SessionLocal
from app.models.query import Query
from datetime import datetime
import os
pytestmark = pytest.mark.asyncio
import httpx
client = httpx.AsyncClient()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def cleanup_db(db_session):
    db_session.query(Query).delete()
    db_session.commit()
    yield
    db_session.query(Query).delete()
    db_session.commit()


@pytest.mark.anyio
async def test_history_returns_entries(db_session):
    # insert a sample entry
    q = Query(
        source_text="A",
        dest_text="B",
        source_lat=1.0,
        source_lon=2.0,
        dest_lat=3.0,
        dest_lon=4.0,
        distance_km=123.45,
        created_at=datetime.utcnow()
    )
    db_session.add(q)
    db_session.commit()

    async with AsyncClient( base_url=BASE_URL) as client:
        resp = await client.get("/history")
        assert resp.status_code == 200
        arr = resp.json()
        assert isinstance(arr, list)
        assert len(arr) >= 1
        item = arr[0]
        assert "source_text" in item
        assert "distance_km" in item
