** HOW to run **

For fastapi to work, you need to install and configure alembic, which performs data migrations for a database organized using sqlalchemy.
Run next in terminal:
- Installation of alembic:
pip install alembic
- Integration of alembic:
alembic init alembic
This will create a directory alembic with related data. Also file alembic.ini will be created in app folder. In this file you should find and modify next line:
- sqlalchemy.url = sqlite:///./city-temperature.db
Also file located at alembic\env.py have to be modified:
- find and change next line: target_metadata = Base.metadata
- in the top of the file, where import is spotted insert next line: from database import Base
Next you should generate initial migrations for DB. For that run in terminal:
- alembic revision --autogenerate -m "Initial migration"
And finally apply migrations to DB, run:
- alembic upgrade head 
From here database file will be created and ready to work. DB file name: city-temperature.db

Finally, run main.py to start this fastapi.
You can get endpoints at http://127.0.0.1:8000/docs


** HOW it is designed **

The working folder contains files common to the project, logically separated by content. 
Also here we have two folders for data about cities and about temperatures, in each of which there are related files with the functionality of the corresponding objects, namely router, crud and schemas. 
Work with an external data source is organized on the openweathermap.org resource, for which I passed free registration and received a free api key that can be replaced with your own, find it at app\degree\openweather.py
Here httpx client is used.
To asynchronously fetch temperature for a number of cities next loop construction was used

import asyncio   

@router.post(path=...,
               tags=...)
async def func(
          db: AsyncSession = Depends(db_manager)
  	):
  	tasks = []

      for object in objects:
          tasks.append(func(db=db))

      await asyncio.gather(*tasks)


Good luck!
