FROM python:3.12

COPY ../../ /app

EXPOSE <<port>> 

# Pip install requirements
RUN pip install -r requirements.txt

RUN python <<app_name>>.py
