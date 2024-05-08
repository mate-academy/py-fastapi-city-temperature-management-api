## Deviations from the task:

I made a decision to use city names instead of id's in the URL address and as a Foreign Key in the Temperature model
the decision is based on dew factors:

* ***URL address***​ *:*

  1. names in URL address is much more informative
  2. it is more intuitive to request city name then look for proper id
  3. and most importantly it is easy for 3rd party automated connections

      _
* ***Foreign Key:***

  1. city names are unique
  2. in case last city in DB is deleted and new one created -> temperature model will relate to the wrong city

## Important aspects:

Following workflows used in project are good to remember ***:***

* ***Alembic***

  1. *<u>alembic.ini</u>*

      sqlalchemy.url uses following format for async DB sqlite+aiosqlite:///./database.db

      _
  2. <u>*to init asynchronous alembic project proper command is*</u>

      ```python
      alembic init --template async alembic
      ```

      where:
      --template used to show that not generic mode is used
      async stands for asynchrous method
      alembic creates "alembic" directory in project's root

      _
  3. <u>*alembic/env.py*</u>  

      in case if we have 2 different models.py modules, 1 of which relates to another by importing ->
      we do not need to import both models to env.py to avoid code duplicating and possible cycled loop

      _
* ***introduction of country column in the city model***

  it is used in order to make the specific web site used in the project recognize the requests,
  please note the doc-string in the appropriate functions

  _
* ***asynchronous loop***

  to asynchronously fetch temperature for a number of cities
  following loop construction was used

  ```python
  import asyncio   
   
  @router.post(path=...,
               tags=...)
  async def func(
          session: AsyncSession = Depends(session_manager)
  	):
  	tasks = []

      for object in objects:
          tasks.append(func(session=session))

      await asyncio.gather(*tasks)
  ```

## Temperature API

* **realisation**:

  the temperature is fetched from the web site using HTML Parsing with the help of:

  1. BeautifulSoup package
  2. aiohttp client

      _
* **limitation**:

  1. Used weather web site might not supply data for all cities, e.g.: Lviv