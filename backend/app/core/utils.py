# backend/app/core/utils.py
import math
import asyncio
from typing import Tuple, Optional
import httpx
from fastapi import HTTPException
import redis.asyncio as aioredis
from app.core.config import REDIS_URL, USER_AGENT

_redis_client: Optional[aioredis.Redis] = None


def get_redis_client() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    return _redis_client


async def geocode_address(address: str) -> Tuple[float, float, int | None, str | None]:
    """
    Geocode a full address using Nominatim /search.
    Caches results in Redis (key: geo:<normalized_address>) for 7 days.
    Returns (lat, lon, osm_id, osm_type)
    Raises HTTPException on failure.
    """
    address_norm = address.strip().lower()
    key = f"geo:{address_norm}"

    redis = get_redis_client()
    cached = await redis.get(key)
    if cached:
        parts = cached.split("|")
        lat = float(parts[0])
        lon = float(parts[1])
        osm_id = int(parts[2]) if parts[2] else None
        osm_type = parts[3] if parts[3] else None
        return lat, lon, osm_id, osm_type

    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1, "addressdetails": 0}
    headers = {"User-Agent": USER_AGENT}

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                r = await client.get(url, params=params, headers=headers)
                r.raise_for_status()
                data = r.json()
                if not data:
                    # Do not cache negatives aggressively; return 404 so client can adjust
                    raise HTTPException(status_code=404, detail=f"Address not found: {address}")
                item = data[0]
                lat = float(item["lat"])
                lon = float(item["lon"])
                osm_id = int(item.get("osm_id")) if item.get("osm_id") else None
                osm_type = item.get("osm_type")
                osm_id_str = str(osm_id) if osm_id is not None else ""
                osm_type_str = osm_type or ""
                await redis.setex(key, 604800, f"{lat}|{lon}|{osm_id_str}|{osm_type_str}")
                return lat, lon, osm_id, osm_type
        except httpx.HTTPStatusError as e:
            if 400 <= e.response.status_code < 500:
                raise HTTPException(status_code=503, detail="Geocoding service returned error")
            await asyncio.sleep(1.0 + attempt * 0.5)
        except (httpx.RequestError, httpx.TimeoutException):
            await asyncio.sleep(1.0 + attempt * 0.5)

    raise HTTPException(status_code=502, detail="Failed to contact geocoding service after retries")


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute haversine distance between two lat/lon pairs, returning kilometers.
    """
    R = 6371.0  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
