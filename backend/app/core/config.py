# backend/app/core/config.py
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:root@localhost:5432/delivery"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))
USER_AGENT = os.getenv("USER_AGENT", "DeliveryDistanceApp/1.0")
RATE_LIMIT_DISTANCE = os.getenv("RATE_LIMIT_DISTANCE", "10/60") 
RATE_LIMIT_HISTORY = os.getenv("RATE_LIMIT_HISTORY", "30/60")  
