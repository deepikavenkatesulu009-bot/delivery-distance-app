from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.query import DistanceRequest, DistanceResponse
from app.core.utils import geocode_address, haversine_distance_km
from app.models.query import Query
from fastapi_limiter.depends import RateLimiter
from app.core.config import RATE_LIMIT_DISTANCE

router = APIRouter()


@router.post(
    "/distance",
    response_model=DistanceResponse,
    dependencies=[Depends(RateLimiter(times=int(RATE_LIMIT_DISTANCE.split("/")[0]),
                                    seconds=int(RATE_LIMIT_DISTANCE.split("/")[1])))]
)
async def calculate_distance(payload: DistanceRequest, db: Session = Depends(get_db)):
    source = payload.source.strip()
    destination = payload.destination.strip()
    unit = payload.unit.lower()
    if unit not in ("km", "mi"):
        raise HTTPException(status_code=400, detail="Unit must be 'km' or 'mi'")

    src_lat, src_lon, src_osm_id, src_osm_type = await geocode_address(source)
    dest_lat, dest_lon, dest_osm_id, dest_osm_type = await geocode_address(destination)

    distance_km = haversine_distance_km(src_lat, src_lon, dest_lat, dest_lon)
    distance = distance_km if unit == "km" else distance_km * 0.621371

    q = Query(
        source_text=source,
        dest_text=destination,
        source_lat=src_lat,
        source_lon=src_lon,
        dest_lat=dest_lat,
        dest_lon=dest_lon,
        distance_km=distance_km,
        osm_source_id=src_osm_id,
        osm_source_type=src_osm_type,
        osm_dest_id=dest_osm_id,
        osm_dest_type=dest_osm_type,
    )
    db.add(q)
    db.commit()
    db.refresh(q)

    return DistanceResponse(
        distance=round(distance, 2),
        unit=unit,
        source_coords=(round(src_lat, 6), round(src_lon, 6)),
        dest_coords=(round(dest_lat, 6), round(dest_lon, 6)),
        status="success",
    )
