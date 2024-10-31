#!/bin/sh

# Wait for PostgreSQL database to be ready
echo "Checking if the PostgreSQL host ($POSTGRES_HOST $POSTGRES_DB_PORT) is ready..."
until nc -z -v -w30 $POSTGRES_HOST $(( $POSTGRES_DB_PORT ));
do
    echo "Waiting for the DB to be ready..."
    sleep 2
done

# SQLAlchemy migrate
echo "Starting database migration..."
alembic revision --autogenerate
alembic upgrade head
echo "Database migration completed successfully."

# docker-compose run --rm migrator
