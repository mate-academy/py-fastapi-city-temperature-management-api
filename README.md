## FastAPI-city-temperature-management-api

### Installing using GitHub

   ```bash
   git clone https://github.com/Veinmax/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Configure Environment Variables:
- Create a .env file in the project root.
- Make sure it includes all the variables listed in the .env.sample file.
- Ensure that the variable names and values match those in the sample file.
   ```bash
   set API_KEY=API_KEY
   alembic upgrade head
   ```
  
Run the Server:
```bash
 uvicorn main:app --reload
```
