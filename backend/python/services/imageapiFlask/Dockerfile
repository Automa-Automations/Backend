FROM python:3.10.14-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:3.10.14-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

WORKDIR /app/services/imageapiFlask
CMD /app/.venv/bin/python main.py
