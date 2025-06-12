FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip && pip install setuptools wheel

COPY requirements.txt .
COPY seed.py /app/seed.py

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "src.main:app", "-c", "src/gunicorn_conf.py"]
