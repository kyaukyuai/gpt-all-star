SERVICE_NAME = gpt-all-star
CODE_DIR = gpt_all_star

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs

shell:
	docker-compose exec $(SERVICE_NAME) /bin/sh

ruff-format:
	poetry run ruff format .

ruff-check:
	poetry run ruff check . --fix

pre-commit-run:
	poetry run pre-commit run --all-files

code-check: ruff-format ruff-check pre-commit-run

.PHONY: build up down logs shell code-check
