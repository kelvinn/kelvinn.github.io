.PHONY: help install test lint format clean migrate run-air-quality run-rain check-db

help:
	@echo "Available commands:"
	@echo "  make install          - Install all dependencies"
	@echo "  make test             - Run unit tests"
	@echo "  make lint             - Run linter (ruff)"
	@echo "  make format           - Format code (ruff)"
	@echo "  make clean            - Clean up cache files"
	@echo "  make migrate          - Run database migrations"
	@echo "  make run-air-quality  - Run air quality monitor"
	@echo "  make run-rain         - Run rain monitor"
	@echo "  make check-db         - Check database connection"

install:
	pip install -r src/requirements.txt

test:
	PYTHONPATH=. pytest tests/ -v

lint:
	ruff check src/ .github/scripts/

format:
	ruff format src/ .github/scripts/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(MESSAGE)"

run-air-quality:
	python .github/scripts/air_quality_monitor.py

run-rain:
	python .github/scripts/rain_monitor.py

check-db:
	@echo "Checking database connection..."
	@if [ -z "$$DATABASE_URL" ]; then \
		echo "ERROR: DATABASE_URL not set"; \
		exit 1; \
	fi
	@echo "Testing connection..."
	pg_isready $$DATABASE_URL || exit 1
	@echo "Running migrations..."
	make migrate
	@echo "Database connection OK"
