from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from logging.config import dictConfig

# imports from your app
from app.core.db import Base, engine
from app.api.routes_distance import router as distance_router
from app.api.routes_history import router as history_router
from app.core.config import REDIS_URL
import redis.asyncio as aioredis
from fastapi_limiter import FastAPILimiter

def setup_logging():
    dictConfig({
        "version": 1,
        "formatters": {"default": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}},
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
        "root": {"level": "INFO", "handlers": ["console"]},
    })

setup_logging()

# create DB tables (will attempt DB connection)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logging.getLogger("uvicorn.error").warning("Could not create DB tables at import time: %s", e)

app = FastAPI(title="Delivery Distance API (MVP)")

# Allow cross-origin for development - tighten this for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (mounted BEFORE static so APIs are not shadowed)
# Use /api prefix to avoid conflict with frontend routes
app.include_router(distance_router, prefix="/api", tags=["distance"])
app.include_router(history_router, prefix="/api", tags=["history"])

# Static mount is added after routers so API routes take precedence
static_dir = os.path.join(os.path.dirname(__file__), "static")  # backend/app/static
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.on_event("startup")
async def startup():
    # initialize fastapi-limiter with redis
    try:
        redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis)
    except Exception as e:
        logging.getLogger("uvicorn.error").warning("FastAPILimiter init failed at startup: %s", e)

@app.get("/health")
def health():
    return {"status": "ok"}
