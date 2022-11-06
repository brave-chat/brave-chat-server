#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "venv                     Create a virtual environment"
	@echo "install                  Install the package and all required core dependencies"
	@echo "run                      Running the app locally"
	@echo "deploy-deta              Deploy the app on a Deta Micro"
	@echo "clean                    Remove all build, test, coverage and Python artifacts"
	@echo "lint                     Check style with pre-commit"
	@echo "test                     Run tests quickly with pytest"
	@echo "test-all                 Run tests on every Python version with tox"
	@echo "build                    Build docker containers services"
	@echo "up                       Spin up the built containers"
	@echo "down                     Stop all running containers"
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
	: `curl -sSL https://install.python-poetry.org | python3 - --uninstall`
	: `rm -rf /home/${USER}/.poetry`
	: `rm -rf /home/${USER}/.pyenv/shims/poetry`
	curl -sSL https://install.python-poetry.org | python3 - --version 1.2.2
	poetry install --only main
	@echo ""

docker-install:
	@echo ""
	@echo "*** installing the required dependencies... ***"
	@echo ""
	@echo ""
	: `curl -sSL https://install.python-poetry.org | python3 - --uninstall`
	: `rm -rf /home/${USER}/.poetry`
	: `rm -rf /home/${USER}/.pyenv/shims/poetry`
	curl -sSL https://install.python-poetry.org | python3 - --version 1.2.2
	/root/.local/bin/poetry install --only main --no-root
	@echo ""

docker-run:
	@echo ""
	@echo "*** Running the app locally... ***"
	@echo ""
	@echo ""
	/root/.local/bin/poetry run server
	@echo ""

run:
	@echo ""
	@echo "*** Running the app locally... ***"
	@echo ""
	@echo ""
	poetry run server
	@echo ""

deploy-deta:
	@echo ""
	@echo "*** Deploying the app on a Deta Micros... ***"
	@echo ""
	@echo "*** Running `deta login`... ***"
	deta login
	@echo "*** Running `deta new .`... ***"
	deta new .
	@echo "*** Running `deta deploy`... ***"
	deta deploy
	@echo "*** Running `deta auth disable`... ***"
	deta auth disable
	@echo "*** Running `deta update -e .env`... ***"
	deta update -e .env
	@echo ""

dist: clean ## builds source and wheel package
	poetry build

build:
	docker compose --file docker-compose.yml build

up:
	docker compose up

down:
	docker compose down

version-major:
	bump2version major

version-minor:
	bump2version minor
