FROM python:3.10.14-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY ./ /app/
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

FROM python:3.10.14-slim-bookworm

WORKDIR /app
COPY --from=builder /app/ ./

EXPOSE 8080

CMD .venv/bin/python services/serpapi/app.py 
