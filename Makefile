.PHONY: dev lint test unit integration e2e clean setup

# Development environment
dev:
	docker-compose up

dev-detached:
	docker-compose up -d

# Linting and formatting
lint:
	cd services/api && python -m black . --line-length 120
	cd services/api && python -m ruff check .
	cd services/api && python -m mypy .
	cd clients/web && npm run lint
	cd clients/mobile && npm run lint

# Testing
test: unit integration

unit:
	cd services/api && python -m pytest tests/unit
	cd clients/web && npm run test
	cd clients/mobile && npm run test

integration:
	docker-compose up -d db
	sleep 5  # Wait for DB to be ready
	cd services/api && python -m pytest tests/integration
	docker-compose down

e2e:
	docker-compose up -d api web
	sleep 10  # Wait for services to be ready
	cd clients/web && npm run test:e2e
	docker-compose down

# Database migrations
migrate:
	cd services/api && alembic upgrade head

migration:
	cd services/api && alembic revision --autogenerate -m "$(m)"

# Setup and cleanup
setup:
	pip install -r services/api/requirements.txt
	cd clients/web && npm install
	cd clients/mobile && npm install

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 