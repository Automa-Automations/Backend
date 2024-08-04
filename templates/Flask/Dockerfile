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
ENV FLASK_APP=main.py
CMD ["/app/.venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]
