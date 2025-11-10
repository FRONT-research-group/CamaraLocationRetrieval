# Makefile for deploying and undeploying docker compose stack

# Load variables from .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

CONF_EXT_NETWORK := ./conf_external_network.sh
REMOVE_EXT_NETWORK := ./remove_external_network.sh
DOCKER_COMPOSE := docker compose

.PHONY:  deploy  deploy-no-auth  undeploy-no-auth  clean  clean-no-auth create-external-network  remove-external-network

conf-ext-network:
	@echo ">>> Running script for configuring external network..."
	$(CONF_EXT_NETWORK)
	@echo ">>> Script finished."

remove-ext-network:
	@echo "Running script for removing external network..."
	$(REMOVE_EXT_NETWORK)
	@echo "Script finished."


deploy: conf-ext-network
	@echo "Running deployment setup..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml up --build -d
	@echo "Deployment complete."

undeploy:
	@echo "Stopping and removing Docker Compose services..."
	$(DOCKER_COMPOSE) -f docker-compose.yaml down
	@echo "Undeployment complete."

clean: undeploy remove-ext-network
	@echo "Cleanup complete."
