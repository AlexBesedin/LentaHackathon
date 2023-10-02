FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .
CMD ["gunicorn", "lenta_main.wsgi:application", "--bind", "0:8000"]