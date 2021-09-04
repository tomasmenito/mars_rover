install:
	poetry install

lint:
	pre-commit run -a

test:
	poetry run pytest .

coverage:
	poetry run pytest --cov .
