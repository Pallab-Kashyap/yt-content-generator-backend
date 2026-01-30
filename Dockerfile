# ---- Base image ----
FROM python:3.11-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- System deps ----
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Working dir ----
WORKDIR /app

# ---- Install deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app ----
COPY app ./app

# ---- Expose port ----
EXPOSE 8000

# ---- Run server ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
