FROM python:3.12

COPY ./ /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD cd services/testservice1Cron;  python main.py
