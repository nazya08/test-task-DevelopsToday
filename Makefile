DC = docker compose


.PHONY: up
up:
	${DC} up -d

.PHONY: build
build:
	${DC} up --build -d

.PHONY: logs
logs:
	${DC} logs -f

.PHONY: stop
stop:
	${DC} stop

.PHONY: down
down:
	${DC} down