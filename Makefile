up:
	docker-compose -f docker-compose.local.yml up --build

down:
	docker-compose -f docker-compose.local.yml down

restart:
	make down
	make start

start:
	docker-compose -f docker-compose.local.yml up -d
