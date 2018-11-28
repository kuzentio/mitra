# WEB_CONTAINER_ID=$(shell docker ps --filter ancestor=mitra_web --format "{{.ID}}")

init:
	docker build -t "gbot" https://github.com/steeply/gbot-trader.git#master
	docker-compose -f docker-compose.local.yml up --build

start:
	docker-compose -f docker-compose.local.yml up -d

stop:
	docker-compose -f docker-compose.local.yml down

restart:
	make stop
	make start

test:
	docker-compose -f docker-compose.local.yml exec web python manage.py test

codestyle:
	docker-compose -f docker-compose.local.yml exec web flake8 .

shell_plus:
	docker-compose -f docker-compose.local.yml exec web python manage.py shell_plus

bash:
	docker-compose -f docker-compose.local.yml exec web bash

# attach:
# 	docker attach $(WEB_CONTAINER_ID)
