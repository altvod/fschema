.PHONY: build-dist format format-check pypi-token-check test upload upload-check

PYTHON ?= python3
PYPI_TOKEN ?=
RUFF ?= ruff
TWINE ?= twine

-include .make.env

build-dist:
	$(PYTHON) -m build

format-check:
	$(RUFF) check .
	$(RUFF) format --check .

format:
	$(RUFF) check . --fix
	$(RUFF) format .

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests

pypi-token-check:
	@test -n "$(PYPI_TOKEN)" || (echo "PYPI_TOKEN is required. Add it to .make.env or export it in your shell."; exit 1)

upload-check: build-dist
	$(TWINE) check dist/*

upload: pypi-token-check upload-check
	@TWINE_USERNAME=__token__ TWINE_PASSWORD="$(PYPI_TOKEN)" $(TWINE) upload dist/*
