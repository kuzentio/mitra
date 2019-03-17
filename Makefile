WEB_CONTAINER_ID=$(shell docker ps -a -q  --filter name=mitra_web)
GBOT_CONTAINER_IDS=$(shell docker ps -a -q --filter ancestor=gbot)

init:
	docker build -t "gbot" https://github.com/steeply/gbot-trader.git#master || true
	docker network create mitra
	docker-compose -f docker-compose.local.yml build

start:
	docker-compose -f docker-compose.local.yml up -d

stop:
	docker rm --volumes --force $(GBOT_CONTAINER_IDS) || true
	docker-compose -f docker-compose.local.yml down

restart:
	make stop
	make start

destroy:
	docker-compose -f docker-compose.local.yml rm -f -s -v

test:
	docker-compose -f docker-compose.local.yml exec web python manage.py test

codestyle:
	docker-compose -f docker-compose.local.yml exec web flake8 .

shell_plus:
	docker-compose -f docker-compose.local.yml exec web python manage.py shell_plus

bash:
	docker-compose -f docker-compose.local.yml exec web bash

attach:
	docker attach $(WEB_CONTAINER_ID)
web-logs:
	docker logs $(WEB_CONTAINER_ID) -f