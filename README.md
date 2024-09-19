# City temperature manager

API on Fastapi, integrated with weatherapi,
that allow to manage cities and fetch current weather for these cities

Project writes with repository pattern to isolate db layer from business logic

# How to run
```shell
python manage.py -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
fastapi dev main
```