# Dockerfile (project root) - multi-stage build (frontend static -> backend container)
###############################################################################
# Stage 1: build frontend static assets
FROM node:20-alpine AS frontend-build

# set PATH using modern ENV syntax
ENV PATH=/src/frontend/node_modules/.bin:$PATH

WORKDIR /src/frontend

# copy frontend package files (both package.json and package-lock.json if present)
COPY frontend/package*.json ./

# install dependencies (npm ci will use package-lock.json if present)
RUN npm ci --silent

# copy frontend source and build
COPY frontend/ .
RUN npm run build

###############################################################################
# Stage 2: build backend image (python)
FROM python:3.11-slim AS backend-build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for psycopg2 and other build needs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# copy backend requirements and install
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# copy backend source into the image
COPY backend/ ./backend

# create static folder and copy frontend build into backend static dir
RUN mkdir -p /app/backend/app/static
COPY --from=frontend-build /src/frontend/build /app/backend/app/static

# expose port (Heroku provides $PORT at runtime)
EXPOSE 8000

# start using gunicorn + uvicorn worker, bind to $PORT (default 8000 locally)
CMD ["sh", "-c", "PORT=${PORT:-8000} && PYTHONPATH=/app/backend exec gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:${PORT} --workers 1 --timeout 120"]
