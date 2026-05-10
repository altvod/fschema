.PHONY: build-dist format format-check test upload upload-check

PYTHON ?= python3
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

upload-check: build-dist
	$(TWINE) check dist/*

upload: upload-check
	$(TWINE) upload dist/*
