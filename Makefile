#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "venv                     Create a virtual environment"
	@echo "install                  Install the package and all required core dependencies"
	@echo "clean                    Remove all build, test, coverage and Python artifacts"
	@echo "lint                     Check style with pre-commit"
	@echo "test                     Run tests quickly with pytest"
	@echo "test-all                 Run tests on every Python version with tox"
	@echo "coverage                 Check code coverage quickly with the default Python"

clean: clean-build clean-pyc clean-test

generate_dot_env:
	@if [[ ! -e .env ]]; then \
		cp .env.example .env; \
	fi

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf .venv; python3 -m venv .venv; source .venv/bin/activate;)
	@echo ""
	@echo "please activate your virtualenv by running:"
	@echo "source .venv/bin/activate"
	@echo ""

lint:
	@echo ""
	@echo "*** Running formatters locally... ***"
	@echo ""
	@echo ""
	tox -ve lint
	@echo ""

test:
	@echo ""
	@echo "*** Running tests locally... ***"
	@echo ""
	@echo ""
	tox -e test
	@echo ""

test-all:
	@echo ""
	@echo "*** Running tests, formatters... ***"
	@echo ""
	@echo ""
	tox
	@echo ""

coverage:
	@echo ""
	@echo "*** Checking code coverage, and generating a report... ***"
	@echo ""
	@echo ""
	tox -e coverage
	poetry run $(BROWSER) htmlcov/index.html
	@echo ""

install: generate_dot_env
	@echo ""
	@echo "*** Generating a .env file and installing the required dependencies... ***"
	@echo ""
	@echo ""
	pip install --upgrade pip
	pip install poetry
	poetry install
	@echo ""

release: dist ## package and upload a release
	poetry publish

dist: clean ## builds source and wheel package
	poetry build

run:
	PYTHONPATH=app/ poetry run server

up: generate_dot_env
	docker-compose build
	docker-compose up -d

down:
	docker-compose down

version-major:
	bump2version major

version-minor:
	bump2version minor
