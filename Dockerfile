FROM python:3.11.6-alpine3.18
LABEL authors="clash"

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "-m", "uvicorn",  "main:app", "--reload"]
