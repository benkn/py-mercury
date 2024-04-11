VENV := .venv
VENV_PYTHON := $(VENV)/bin/python

run:
	$(VENV_PYTHON) main.py

$(VENV): # Creates the virtual environment if it is not made already
	@echo "$(GREEN)Creating virtual environment$(NO_COLOR)"
	@python3 -m venv $(VENV)

## TODO Add tasks for creating template files for first time initi
init: $(VENV) ## initializes the project
	@echo "$(GREEN)Installing dependencies$(NO_COLOR)"
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

test: ## runs the unit tests
	@$(VENV_PYTHON) -m pytest

lint: ## reviews the code for linting errors
	@echo "💅 $(MAGENTA)Linting files$(NO_COLOR)"
	@ruff check .
	@echo "😍 $(YELLOW)Beautiful files$(NO_COLOR)"

help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-10s$(NO_COLOR) %s\n", $$1, $$2}'


# Colors
## The ;01m makes the font bold
NO_COLOR=\x1b[0m
BLUE=\x1b[0m
BLACK=\x1b[30;01m
RED=\x1b[31;01m
GREEN=\x1b[32;01m
YELLOW=\x1b[33;01m
BLUE=\x1b[34;01m
MAGENTA=\x1b[35;01m
CYAN=\x1b[36;01m
WHITE=\x1b[37;01m