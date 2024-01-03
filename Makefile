# Generate makefile commands to build the project and run the project

# Project variables
IMAGE_NAME := mixrai
CONTAINER_NAME := django-app
PORT := 8000

# Build the Docker image
build:
	@docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	@docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME)

# Stop the running Docker container
stop:
	@docker stop $(CONTAINER_NAME)

# Remove the Docker container
clean:
	@docker rm $(CONTAINER_NAME)

# Remove the Docker image
clean-image:
	@docker rmi $(IMAGE_NAME)

# Enter the Docker container's shell
shell:
	@docker exec -it $(CONTAINER_NAME) /bin/sh

# Makefile commands
.PHONY: build run stop clean clean-image shell


# Makefile for managing Docker Compose operations

# Project variables
COMPOSE_FILE := docker-compose.yml

# Start the containers in the background
up:
	docker-compose up

# Start the containers in the foreground
up-background:
	docker-compose -f $(COMPOSE_FILE) up -d

# Rebuild the containers and start
build-up:
	docker-compose -f $(COMPOSE_FILE) up --build -d

# Stop the running containers
down:
	docker-compose -f $(COMPOSE_FILE) down

# Stop the containers and remove volumes
down-volumes:
	docker-compose -f $(COMPOSE_FILE) down -v

# View output from containers
logs:
	docker-compose -f $(COMPOSE_FILE) logs

# Follow log output
logs-follow:
	docker-compose -f $(COMPOSE_FILE) logs -f

# Execute the command inside the Django app container
exec:
	docker-compose -f $(COMPOSE_FILE) exec djangoapp bash

# Makefile commands
.PHONY: up up-foreground build-up down down-volumes logs logs-follow exec
