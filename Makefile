all: run

run:
	docker-compose build main
	docker-compose run main
