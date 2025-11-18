.PHONY: install build up down logs test lint fmt k8s-apply k8s-delete

install:
	pip install -r requirements.txt -r requirements-dev.txt

build:
	docker-compose -f infra/docker-compose.yml build --parallel

up:
	docker-compose -f infra/docker-compose.yml up --build -d

down:
	docker-compose -f infra/docker-compose.yml down -v

logs:
	docker-compose -f infra/docker-compose.yml logs -f

test:
	pytest -q

lint:
	flake8 --max-line-length=88 --extend-ignore=E203,W503
	mypy . --ignore-missing-imports --strict

fmt:
	black .
	isort .

k8s-apply:
	kubectl apply -f infra/k8s/

k8s-delete:
	kubectl delete -f infra/k8s/
