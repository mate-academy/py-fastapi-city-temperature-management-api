import time
from sqlalchemy.exc import OperationalError
from database import engine


def wait_for_db(max_retries=10, delay=2):
    for attempt in range(max_retries):
        try:
            connection = engine.connect()
            connection.close()
            print("Database is ready!")
            return
        except OperationalError:
            print(f"Database not ready, retry {attempt + 1}/{max_retries}...")
            time.sleep(delay)
    raise Exception("Database not available after retries")


if __name__ == "__main__":
    wait_for_db()
