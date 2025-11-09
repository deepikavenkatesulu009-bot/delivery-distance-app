from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import Base, engine
from app.api.routes_distance import router as distance_router
from app.api.routes_history import router as history_router
from app.core.config import REDIS_URL, APP_HOST, APP_PORT
import redis.asyncio as aioredis
from fastapi_limiter import FastAPILimiter
import logging
from logging.config import dictConfig

def setup_logging():
    dictConfig({
        "version": 1,
        "formatters": {"default": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}},
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
        "root": {"level": "INFO", "handlers": ["console"]},
    })

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delivery Distance API (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(distance_router, prefix="", tags=["distance"])
app.include_router(history_router, prefix="", tags=["history"])
