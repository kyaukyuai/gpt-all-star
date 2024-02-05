build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs

shell:
	docker-compose exec gpt-all-star /bin/sh

.PHONY: build up down logs shell
