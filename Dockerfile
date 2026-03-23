FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTOCODE=1 \ 
PYTHONUNBUFFERED=1

WORKDIR /webapp

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]