migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

dev:
	uvicorn src.main:app --reload
