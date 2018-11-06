up:
	docker-compose -f docker-compose.local.yml up --build

down:
	docker-compose -f docker-compose.local.yml down

restart:
	make down
	make start

start:
	docker-compose -f docker-compose.local.yml up -d

test:
	docker-compose -f docker-compose.local.yml exec web python manage.py test

codestyle:
	flake8 .

shell_plus:
	docker-compose -f docker-compose.local.yml exec web python manage.py shell_plus

bash:
	docker-compose -f docker-compose.local.yml exec web bash
