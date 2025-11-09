from pydantic import BaseModel, Field
from typing import Tuple, Optional
from datetime import datetime


class DistanceRequest(BaseModel):
    source: str = Field(..., min_length=5, description="Full source address")
    destination: str = Field(..., min_length=5, description="Full destination address")
    unit: str = Field("km", description="Unit: 'km' or 'mi'")

    class Config:
        schema_extra = {
            "example": {
                "source": "1600 Amphitheatre Parkway, Mountain View, CA",
                "destination": "1 Apple Park Way, Cupertino, CA",
                "unit": "mi",
            }
        }


class DistanceResponse(BaseModel):
    distance: float
    unit: str
    source_coords: Tuple[float, float]
    dest_coords: Tuple[float, float]
    status: str


class HistoryItem(BaseModel):
    id: int
    source_text: str
    dest_text: str
    distance_km: float
    created_at: datetime
