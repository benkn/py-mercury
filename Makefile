run:
	@python3 main.py

init: ## initializes the project
	@./.bin/init.sh
	@echo "Now run source ./.venv/bin/activate"

test: ## runs the unit tests
	@echo "Running tests"
	python3 -m pytest

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