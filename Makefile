# Makefile for deploying and undeploying docker compose stack

# Load variables from .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

DOCKER_COMPOSE := docker compose

.PHONY:  deploy  deploy-no-auth  undeploy-no-auth  clean  clean-no-auth

deploy:
	@echo "Running deployment setup..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml up --build -d
	@echo "Deployment complete."

undeploy:
	@echo "Stopping and removing Docker Compose services..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml down
	@echo "Undeployment complete."

clean: undeploy
	@echo "Cleanup complete."
