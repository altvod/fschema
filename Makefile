.PHONY: format format-check test

PYTHON ?= python3
RUFF ?= ruff

format-check:
	$(RUFF) check .
	$(RUFF) format --check .

format:
	$(RUFF) check . --fix
	$(RUFF) format .

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests
