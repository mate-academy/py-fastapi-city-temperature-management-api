import httpx
from sqlalchemy.orm import Session
from app.models import City, Temperature


async def fetch_and_store_temperatures(db: Session) -> list[Temperature]:
    """Асинхронно отримує поточну температуру для всіх міст та зберігає в БД."""
    cities = db.query(City).all()
    if not cities:
        return []

    new_records = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                # Отримання даних з публічного API погоди wttr.in
                response = await client.get(
                    f"https://wttr.in/{city.name}?format=j1", timeout=5.0
                )
                if response.status_code == 200:
                    data = response.json()
                    current_condition = data.get("current_condition", [{}])[0]
                    temp_str = current_condition.get("temp_C", "20.0")
                    temp_val = float(temp_str)
                else:
                    temp_val = 20.0
            except Exception:
                # Резервне значення, якщо запит не вдався
                temp_val = 20.0

            temperature_record = Temperature(
                city_id=city.id,
                temperature=temp_val
            )
            db.add(temperature_record)
            new_records.append(temperature_record)

    db.commit()
    for record in new_records:
        db.refresh(record)

    return new_records
