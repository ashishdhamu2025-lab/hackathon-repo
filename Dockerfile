FROM python:3.12-slim

WORKDIR /app

# System deps (if you add OCR/PDF tools later, install them here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

ENV PYTHONUNBUFFERED=1
# Cloud Run injects PORT; default to 8080 for local runs
ENV PORT=8080

# Use exec form + shell to expand $PORT
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1