from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.db import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    source_text = Column(String, nullable=False)
    dest_text = Column(String, nullable=False)
    source_lat = Column(Float, nullable=True)
    source_lon = Column(Float, nullable=True)
    dest_lat = Column(Float, nullable=True)
    dest_lon = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    osm_source_id = Column(Integer, nullable=True)
    osm_source_type = Column(String, nullable=True)
    osm_dest_id = Column(Integer, nullable=True)
    osm_dest_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
