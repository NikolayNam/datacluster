#!/bin/sh

# echo "Running Alembic migrations..."
# Запуск миграции Alembic
# alembic upgrade head

# Запуск приложения
exec python master.py
