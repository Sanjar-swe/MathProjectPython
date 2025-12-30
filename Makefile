.PHONY: help up down build logs migrate superuser

help:
	@echo "Available commands:"
	@echo "  make up         - Start all services (Django + Bot + Postgres)"
	@echo "  make down       - Stop all services"
	@echo "  make build      - Build/Rebuild containers"
	@echo "  make logs       - Show logs"
	@echo "  make migrate    - Run Django migrations"
	@echo "  make superuser  - Create Django superuser"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up -d --build

logs:
	docker-compose logs -f

migrate:
	docker-compose exec web python manage.py migrate

superuser:
	docker-compose exec web python manage.py createsuperuser
