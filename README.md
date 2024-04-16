## FastAPI City Temperature Management API

### Installing using GitHub

   ```bash
   git clone https://github.com/cth-usq/py-fastapi-city-temperature-management-api.git
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Configure Environment Variables:
   
### Create a .env file in the project root.
   ```bash
   set API_KEY=API_KEY
   alembic upgrade head
   ```

Run the Server:
```bash
 uvicorn main:app --reload
```
