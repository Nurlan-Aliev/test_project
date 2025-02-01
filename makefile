migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head