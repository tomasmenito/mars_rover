install:
	poetry install

poetry-shell:
	poetry shell

docker-build:
	docker build -t mars_rover --rm . 
docker-shell:
	docker run -it --name mars_rover --rm mars_rover

lint:
	pre-commit run -a

test:
	pytest .

coverage:
	pytest --cov .
