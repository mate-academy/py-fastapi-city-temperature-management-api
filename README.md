## Temperature management API
Management of city data and temperature data on the FastAPI framework. 

### Description of mechanics:
- CRUD (Create, Read, Update, Delete) API for city data management.
- API,
which gets the current temperature data for all cities in the database and stores this data in the database (open-meteo service).
- Provides all temperature data.

## Launching the program 

- `python -m venv venv` - activate virtual environment
- `venv\Scripts\activate` - Windows
- `source venv/bin/activate` - macOS/Linux
- `pip install -r requirements.txt` - install all library
- `alembic revision --autogenerate -m "Initial clean migration"` - generate a migration file
- `alembic upgrade head` - apply migration to the database

## Screenshot

<img width="717" height="626" alt="Знімок екрана 2026-09-14 092606" src="https://github.com/user-attachments/assets/7b672875-e5ea-4def-bc27-0c88ae4403d4" />

<img width="718" height="446" alt="Знімок екрана 2026-09-14 092631" src="https://github.com/user-attachments/assets/5255c12e-f5a7-4264-9c20-76a88bde52c8" />

<img width="720" height="548" alt="Знімок екрана 2026-09-14 092646" src="https://github.com/user-attachments/assets/6be1051a-4d23-4976-9637-cd849ab15b08" />

<img width="715" height="620" alt="Знімок екрана 2026-09-14 092738" src="https://github.com/user-attachments/assets/0eed9785-f2bd-4887-8042-1169c293aa54" />

<img width="712" height="446" alt="Знімок екрана 2026-09-14 092804" src="https://github.com/user-attachments/assets/3f532214-f328-4ab3-a6b9-1accc61f76d2" />

<img width="717" height="502" alt="Знімок екрана 2026-09-14 092855" src="https://github.com/user-attachments/assets/09bd4a4d-923a-4c51-b8f0-8f8c23a4fca4" />

<img width="715" height="497" alt="Знімок екрана 2026-09-14 092953" src="https://github.com/user-attachments/assets/b1533514-e7d1-4cfc-b51d-2cf691537b35" />

<img width="721" height="416" alt="Знімок екрана 2026-09-14 093008" src="https://github.com/user-attachments/assets/f5b59af7-09ac-4af3-aed3-ef1bf278a430" />
