FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PORT=8000 \
    EXECUTION_BACKEND=subprocess \
    WORKSPACES_ROOT=/tmp/erettsegi-workspaces \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Cloud Run sets PORT (usually 8080); Compose uses 8000.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
