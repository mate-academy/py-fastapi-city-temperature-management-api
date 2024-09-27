FROM python:3.12-alpine3.20
LABEL maintainer="cven28@gmail.com"

ENV PYTHONNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . app/
