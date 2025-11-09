from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.query import Query
from app.schemas.query import HistoryItem
from fastapi_limiter.depends import RateLimiter
from app.core.config import RATE_LIMIT_HISTORY

router = APIRouter()


@router.get("/history", response_model=list[HistoryItem],
            dependencies=[Depends(RateLimiter(times=int(RATE_LIMIT_HISTORY.split("/")[0]),
                                            seconds=int(RATE_LIMIT_HISTORY.split("/")[1])))])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    limit = min(max(1, limit), 100)
    rows = db.query(Query).order_by(Query.created_at.desc()).limit(limit).all()
    results = []
    for r in rows:
        results.append(HistoryItem(
            id=r.id,
            source_text=r.source_text,
            dest_text=r.dest_text,
            distance_km=round(r.distance_km, 3) if r.distance_km is not None else 0.0,
            created_at=r.created_at
        ))
    return results
