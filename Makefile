# Define variables
PYTHON := python3
VENV := ".venv"

# Declare phony targets
.PHONY: help install-poetry install setup-poetry test clean

# Display help information
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs -I {} awk 'BEGIN {FS = ":.*?## "} /^{}:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Install poetry
install-poetry:
	@echo "Installing poetry..."
	@curl -sSL https://install.python-poetry.org | $(PYTHON) -
	@if [ -f ${HOME}/.poetry/env ]; then \
		$(eval include ${HOME}/.poetry/env); \
	else \
		echo "Poetry environment file not found!"; exit 1; \
	fi

# Install dependencies
install: ## Install dependencies
	@echo "Installing..."
	@if [ "$(shell which poetry)" = "" ]; then \
		$(MAKE) install-poetry; \
	fi
	@$(MAKE) setup-poetry

# Set up poetry
setup-poetry: ## Set up poetry environment and install dependencies
	@poetry env use $(PYTHON)
	@poetry config virtualenvs.in-project true
	@poetry install

# Run tests
test:  ## Run tests
	@poetry run pytest

# Clean the project
clean: ## Clean the virtual environment, delete the lock file, and remove all *.pyc files
	@echo "Cleaning the virtual env and deleting the lock file..."
	@if [ -d $(VENV) ]; then rm -r $(VENV); fi
	@if [ -f poetry.lock ]; then rm poetry.lock; fi
	@find . -iname "*.pyc" -delete