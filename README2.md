## Project Description
Application that tracks temperature data for cities. Written with FastAPI&SqlAlchemy.

## How to run
1. In project directory create .env file, copy fields from env.sample file to .env and populate fields with your data.
2. Run terminal command ```pip install -r requirements.txt```
3. After successful installation, run ```uvicorn main:app```
4. Your API is ready and running at ```127.0.0.1:8000``` with documented endpoints at ```127.0.0.1:8000/docs/```