FROM python:3.14.2-alpine

LABEL mainteiner="sserebriy@gmail.com"

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home fastapi-user --gecos ""

COPY . .

USER fastapi-user
