## Інструкція з запуску

1. **Створіть та активуйте віртуальне середовище**:
   ```bash
   py -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   
