# backend/tests/test_distance.py
import pytest
from httpx import AsyncClient
from app.main import app
from app.core.db import Base, engine, SessionLocal
from app.models.query import Query
from sqlalchemy.orm import Session
import asyncio
import os
pytestmark = pytest.mark.asyncio
import httpx
client = httpx.AsyncClient()


# Use a separate test DB in real CI; here we use same DB for simplicity in local runs
# Create tables for test
Base.metadata.create_all(bind=engine)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def cleanup_db(db_session: Session):
    # clear queries table before each test
    db_session.query(Query).delete()
    db_session.commit()
    yield
    db_session.query(Query).delete()
    db_session.commit()


@pytest.mark.anyio
async def test_distance_endpoint_monkeypatched(monkeypatch):
    """
    Test /distance while monkeypatching geocode_address to avoid external HTTP.
    """
    async def fake_geocode(addr: str):
        # Return lat, lon, osm_id, osm_type
        if "1600 amphitheatre" in addr.lower():
            return 37.422033, -122.084125, 12345, "way"
        if "apple park" in addr.lower() or "1 apple park" in addr.lower():
            return 37.334924, -122.009020, 98765, "way"
        # default
        return 0.0, 0.0, None, None

    monkeypatch.setattr("app.core.utils.geocode_address", fake_geocode)

    async with AsyncClient(base_url=BASE_URL) as client:
        payload = {
            "source": "1600 Amphitheatre Parkway, Mountain View, CA",
            "destination": "1 Apple Park Way, Cupertino, CA",
            "unit": "mi"
        }
        resp = await client.post("/distance", json=payload)
        print(resp.status_code,resp.text)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert "distance" in data
        # Expect a small distance in miles (approx ~7-10 miles)
        assert data["distance"] > 1
