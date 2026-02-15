.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run:
	uvicorn app.main:app --reload

.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	flake8
	isort -qc .

.PHONY: fix
fix:
	isort .

.PHONY: check
check: lint test

.PHONY: migrate
migrate:
	@read -p "Введите сообщение для миграции: " message; \
	alembic revision --autogenerate -m "$$message"
	alembic upgrade head

.PHONY: migrate-auto
migrate-auto:
	alembic revision --autogenerate -m "Auto migration"
	alembic upgrade head

.PHONY: migrate-up
migrate-up:
	alembic upgrade head

.PHONY: migrate-down
migrate-down:
	alembic downgrade -1

.PHONY: migrate-status
migrate-status:
	alembic current

.PHONY: migrate-history
migrate-history:
	alembic history --verbose
