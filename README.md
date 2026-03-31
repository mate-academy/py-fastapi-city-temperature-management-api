# 🌦️ Weather & Temperature Tracker API

> A modern asynchronous API for temperature monitoring, built with **FastAPI + SQLAlchemy 2.0**.  
> This project focuses on high performance, correct timezone handling, and architectural clarity.

---

## 🚀 Key Features

| Feature | Description |
|---------|------|
| ⚡ **Fully Asynchronous** | Leverages `AsyncSession` for all database operations to ensure non-blocking I/O|
| 📦 **High Performance** | Implements efficient batch creation using `session.execute(insert(...), data_list)`, significantly faster than standard loops|
| 🔗 **Eager Loading** | Utilizes `joinedload` and `selectinload` strategies to prevent `MissingGreenlet` errors and solve the N+1 problem |
| 🔄 **Circular Import-Free Architecture** | Pydantic models are split into `Base` and `Read` levels, ensuring stability and excellent IDE support without runtime rebuilds |
| 🗑️ **Atomic Operations** | Deletions and lookups use SQL subqueries (`scalar_subquery`) for maximum precision and data integrity |

---

## 🛠️ Technology Stack

- **Framework** — [FastAPI](https://fastapi.tiangolo.com/)
- **ORM** — SQLAlchemy 2.0 (Async)
- **Validation** — Pydantic V2
- **Migrations** — Alembic
- **Database** — SQLite (Async)

---

## ⚙️ Quick Start

### 1. Environment Setup

Clone the repository and create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Database Migrations

Run migrations to set up the table structure (including automatic timestamp generation at the DB level):

```bash
alembic upgrade head
```

### 3. Run the Server

```bash
uvicorn src.main:app --reload
```
