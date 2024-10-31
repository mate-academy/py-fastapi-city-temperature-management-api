#!/usr/bin/env python

import typer
import asyncio
from src.db.seed_data import seed_data

app = typer.Typer()

@app.command()
def seed():
    """Seed the database with initial data."""
    asyncio.run(seed_data())

if __name__ == "__main__":
    typer.run(seed)
