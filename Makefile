install:
	poetry install

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
