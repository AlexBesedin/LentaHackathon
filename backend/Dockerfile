FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip3 install -r requirements.txt --no-cache-dir \
    && apt-get purge -y --auto-remove gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
CMD ["gunicorn", "lenta_main.wsgi:application", "--bind", "0:8000"]