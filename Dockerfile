FROM python:3.10

WORKDIR /usr/src/fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR off

RUN apt-get update && apt-get install -y gcc libpq-dev netcat-openbsd

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY entrypoint.sh /entrypoint.sh
COPY migration_script.sh /migration_script.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /migration_script.sh
