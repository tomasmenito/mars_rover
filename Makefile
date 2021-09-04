install:
	poetry install

test:
	poetry run pytest .

coverage:
	poetry run pytest --cov .
