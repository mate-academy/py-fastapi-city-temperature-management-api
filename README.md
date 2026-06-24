# City & Temperature Management API

A FastAPI application that manages city records and automatically tracks historical temperature data by integrating with an external weather service.

---

## 🚀 Installation & Run Instructions

###  Clone the repository and create a virtual environment:

```bash
git clone https://github.com/amesemyta1/py-fastapi-city-temperature-management-api/tree/develop
cd py-fastapi-city-temperature-management-api
python -m venv .venv

Activate the virtual environment:
Windows: .venv\Scripts\activate
Linux/macOS: source .venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Start the Server
uvicorn app.main:app --reload
```
## 🧠 Assumptions & Simplifications

* **External Weather Resource:** The **Open-Meteo API** (along with its Geocoding API) was selected because it is completely free and requires no API keys, ensuring instant local testing for evaluators.
* **Fault-Tolerant Bulk Updates:** The `POST /temperatures/update` endpoint processes cities sequentially in a loop. If an external API request fails for a specific city, the application catches the error gracefully, appends it to an error summary, and continues updating the rest.
* **Optimized Transactions:** In the update loop, the database transaction is intentionally committed exactly once at the end of the operation rather than per city. This minimizes disk write overhead.
* **Cascade Constraints:** Deleting a city via `DELETE /cities/{city_id}` automatically triggers a cascade deletion of all historical temperature rows belonging to that city, maintaining proper referential integrity.
* **Time Zone Consistency:** All recorded temperatures are timestamped using UTC time (`datetime.datetime.utcnow`) to avoid server/client time zone discrepancies.