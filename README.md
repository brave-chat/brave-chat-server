# Brave Chat Server

![Vercel](https://vercelbadge.vercel.app/api/wiseaidev/fastapi-singlestore-backend)
![Codeql](https://github.com/github/docs/actions/workflows/codeql.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/wiseaidev/fastapi-singlestore-backend/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/wiseaidev/fastapi-singlestore-backend/tree/main)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/wiseaidev/fastapi-singlestore-backend/main.svg)](https://results.pre-commit.ci/latest/github/wiseaidev/fastapi-singlestore-backend/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Architecture](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/32lsb1pwom7ch3yx0yxi.jpg)](https://github.com/wiseaidev/fastapi-singlestore-backend)

A Fully Async based backend for the [react chat application](https://github.com/wiseaidev/chat). It is a multi-model server that is fully functional and supports all the usual messaging app capabilities such as of one-on-one (private) and room messaging. It enables users to send text and multimedia messages(e.g. images). Also, users can freely create, join, and leave chat rooms where everyone can message each other.

## Table of Contents

- [Features](#features)
- [Development Requirements](#development-requirements)
- [Project Structure](#project-structure)
- [Installation with Make](#installation-with-make)
  - [1. Create a virtualenv](#1-create-a-virtualenv)
  - [2. Activate the virtualenv](#2-activate-the-virtualenv)
  - [3. Install dependencies](#3-install-dependencies)
  - [4. Setup a SingleStore account](#4-setup-a-singlestore-account)
  - [5. Set your SingleStore Credentials](#5-set-your-singlestore-credentials)
  - [6. Setup a Redis account](#6-setup-a-redis-account)
  - [7. Set your Redis Cloud Credentials](#7-set-your-redis-cloud-credentials)
  - [8. Generate a secret key](#8-generate-a-secret-key)
  - [9. Set your Deta project key](#9-set-your-deta-project-key)
  - [10. Generate a secret key](#10-generate-a-secret-key)
  - [11. Run The Project Locally](#11-run-the-project-locally)
- [Running locally with Compose v2](#running-locally-with-compose-v2)
- [Access Swagger Documentation](#access-swagger-documentation)
- [Access Redocs Documentation](#access-redocs-documentation)
- [Access Prometheus Metrics](#access-prometheus-metrics)
- [Access Grafana Dashboard](#access-grafana-dashboard)
- [Cloud Deployments](#cloud-deployments)
  - [Deta Micros (Not Possible)](#deta-micros-not-possible)
  - [Heroku](#heroku)
  - [Vercel (Not Possible)](#vercel-not-possible)
  - [Netlify (Not Possible)](#netlify-not-possible)
- [Core Dependencies](#core-dependencies)
- [TODO and Contributions](#todo-and-contributions)
- [License](#license)

## Features

This project supports the following features:

- Create, join rooms.
- Multi-model Database.
- Highly scalable architecture.
- Changing user profile information.
- Add, remove users to/from contacts list.
- Sending an Receiving images in real time.
- Sending an Receiving text messages in real time.
- Unicast messaging (e.g. Sending private messages).
- A pub/sub Redis architecture built on top of web-sockets.
- Broadcast messaging (e.g. Sending messages in a chat room).
- A Monolith architecture, but its modularity allows it to be divided into microservices.
- Full control over your messages with the ability to create, delete, and edit them as you please.

## Development Requirements

- Make (GNU command)
- Python (>= 3.8)
- Poetry (1.2)

## Project Structure

<details>
<summary><code>❯ tree app</code></summary>

```sh
.
├── auth     # Package contains different config files for the `auth` app.
│   ├── crud.py     # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different data models for ORM to interact with database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py     # Module contains different schemas for this api for validation purposes.
├── chats     # Package contains different config files for the `chats` app.
│   ├── crud.py     # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different data models for ORM to interact with database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py     # Module contains different schemas for this api for validation purposes.
├── config.py     # Module contains the main configuration settings for project.
├── contacts     # Package contains different config files for the `contacts` app.
│   ├── crud.py     # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different data models for ORM to interact with the database.
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py     # Module contains different schemas for this api for validation purposes.
├── __init__.py
├── main.py     # Startup script. Starts uvicorn.
├── rooms     # Package contains different config files for the `rooms` app.
│   ├── crud.py     # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different models for ORMs to inteact with database..
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py     # Module contains different schemas for this api for validation purposes.
├── users     # Package contains different config files for the `users` app.
│   ├── crud.py     # Module contains different CRUD operations performed on the database.
│   ├── models.py     # Module contains different models for ORMs to inteact with database..
│   ├── router.py     # Module contains different routes for this api.
│   └── schemas.py     # Module contains different schemas for this api for validation purposes.
├── utils     # Package contains different common utility modules for the whole project.
│   ├── constants.py
│   ├── crypt_util.py
│   ├── db_utils.py     # A utility script that create, drop a test database used in the tests package.
│   ├── dependencies.py     # A utility script that yield a session for each request to make the crud call work.
│   ├── engine.py     # A utility script that initialize two sqlalchemy engines and set them as app state variables.
│   ├── full_text_search.py     # A utility script to make sqlalchemy and singlestore compatible for implementing full text search on a given table.
│   ├── jwt_util.py     # A utility script for JWT.
│   ├── mixins.py     # A utility script that contains common mixins for different models.
│   └── pub_sub_handlers.py     # A utility script that contains publishers and consumers handlers for the redis queue.
└── web_sockets     # Package contains different config files for the `web_sockets` app.
    └── router.py     # Module contains different routes for the websockets.
```

</details>

## Installation with Make

The best way to configure, install main dependencies, and run the project is by using `make`. So, make sure you have `make` installed and configured on your machine. If it is not the case, head over to [this thread](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows) on stackoverflow to install it on windows, or [this thread](https://stackoverflow.com/questions/11494522/installing-make-on-mac) to install it on Mac OS.

Having `make` installed and configured on your machine, you can now run `make` under the root directory of this project to explore different available commands to run:

```sh
make

Please use 'make <target>' where <target> is one of:

venv                     Create a virtual environment
install                  Install the package and all required core dependencies
run                      Running the app locally
deploy-deta              Deploy the app on a Deta Micro
clean                    Remove all build, test, coverage and Python artifacts
lint                     Check style with pre-commit
test                     Run tests quickly with pytest
test-all                 Run tests on every Python version with tox
coverage                 Check code coverage quickly with the default Python
```

### 1. Create a virtualenv

```sh
make venv
```

### 2. Activate the virtualenv

```sh
source .venv/bin/activate
```

### 3. Install dependencies

```sh
make install
```

**Note**: _This command will automatically generate a `.env` file from `.env.example`, uninstall the old version of poetry on your machine, then install latest version `1.2.2`, and install the required main dependencies._

### 4. Setup a SingleStore account

You can refer to [this tutorial](https://dev.to/wiseai/a-deep-dive-into-connecting-fastapi-with-singlestore-2dn8#setting-up-singlestore) to create a SingleStore account and a MySQL `chat` database.

### 5. Set your SingleStore Credentials

Fill in the following environment variables in your .env file accordingly:

```yaml
# Database
SINGLESTORE_USERNAME=admin
SINGLESTORE_PASSWORD=<database password>
SINGLESTORE_HOST=<database name>
SINGLESTORE_PORT=3306
SINGLESTORE_DATABASE=<database name>
```

### 6. Setup a Redis account

Create a free account on [Redis Cloud](https://redis.info/try-free-dev-to).

### 7. Set your Redis Cloud Credentials

Set the following environment variables in your .env file according to your account credentials:

```yaml
# REDIS
# USER IN REDIS CLOUD
REDIS_USERNAME=default
# DATABASE PASSWORD
REDIS_PASSWORD=<database password>
# REDIS HOST
REDIS_HOST=<redis url>
# REDIS PORT
REDIS_PORT=15065
```

### 8. Generate a secret key

Create a free account on [Deta](https://www.deta.sh/), and create a new project.

### 9. Set your Deta project key

Set the following environment variable in your `.env` file according to your project key value:

```yaml
# Deta
DETA_PROJECT_KEY=
```

### 10. Generate a secret key

Generate a secret key using openssl and update its env var in .env file.

```sh
openssl rand -hex 128

afa1639545d53ecf83c9f8acf4704abe1382f9a9dbf76d2fd229d4795a4748712dbfe7cf1f0a812f1c0fad2d47c8343cd1017b22fc3bf43d052307137f6ba68cd2cb69748b561df846873a6257e3569d6307a7e022b82b79cb3d6e0fee00553d80913c1dcf946e2e91e1dfcbba1ed9f34c9250597c1f70f572744e91c68cbe76
```

```yaml
# App config:
JWT_SECRET_KEY=afa1639545d53ecf83c9f8acf4704abe1382f9a9dbf76d2fd229d4795a4748712dbfe7cf1f0a812f1c0fad2d47c8343cd1017b22fc3bf43d052307137f6ba68cd2cb69748b561df846873a6257e3569d6307a7e022b82b79cb3d6e0fee00553d80913c1dcf946e2e91e1dfcbba1ed9f34c9250597c1f70f572744e91c68cbe76
DEBUG=False
```

### 11. Run The Project Locally

```sh
make run
```

## Running locally with Compose v2

Make sure your have [compose v2](https://github.com/docker/compose) installed and configured on your machine, and run the following command to build the predefined docker services(make sure you have a .env file beforehand):

**Using Make**

```sh
make docker-build
```

or simply running:

```
docker compose build
```

Once that is done, you can spin up the container:

**Using Make**

```sh
make up
```

or running:

```
docker compose up
```

## Access Swagger Documentation

> <http://localhost:8000/docs>

## Access Redocs Documentation

> <http://localhost:8000/redocs>

## Access Prometheus Metrics

> <http://localhost:8000/metrics>

## Access Grafana Dashboard

> <http://localhost:3001>

## Cloud Deployments

## Deta Micros (Not Possible)

To use the Deta version of the APIs you'll need to create a Deta account.

[![Deploy on Deta](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/wiseaidev/fastapi-singlestore-backend)

#### Deta CLI (Not Possible)

Make sure you have Deta cli installed on your machine. If it is not the case, just run the following command(on a linux distro or Mac):

```sh
curl -fsSL https://get.deta.dev/cli.sh | sh
```

Manually add `/home/<user_name>/.deta/bin/deta` to your path:

```sh
PATH="/home/<user_name>/.deta/bin:$PATH"
```

Now you can deploy the app on a Deta Micro:

```sh
make deploy-deta
```

You can then use the Deta UI to check the logs and the URL the API is hosted on.

**Notes**:

- _Make sure your `.env` file is being provided with valid env vars values accordingly._

- _The `main.py` file is used as an entry point for deta. Same goes for `requirements.txt`._

- _Deta Micros are limited to 512MB per deployment._

### Heroku

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wiseaidev/fastapi-singlestore-backend)

#### Heroku CLI (Not Possible)

Before going any further, make sure you already installed and configured the Heroku CLI on you machine. If it is not the case, you can install it on Ubuntu using the followig command:

```sh
sudo wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
```

Now, you need to install the Heroku container registry plugin:

```sh
heroku plugins:install heroku-container-registry
```

Once that completed, Login to your registry:

```sh
heroku container:login
```

Set your env variables from the `.env` file:

```sh
xargs -a .env -I {} heroku config:set {}
```

Log in to the Heroku Docker registry before.

```sh
heroku auth:token | docker login --username=_ registry.heroku.com --password-stdin
```

Build your container images:

```sh
docker build tag lb -f Dockerfile.haproxy
docker tag app1 registry.heroku.com/fastapi-singlestore-backend_app1/web
docker tag app2 registry.heroku.com/fastapi-singlestore-backend_app2/web
docker tag app3 registry.heroku.com/fastapi-singlestore-backend_app3/web
docker tag app4 registry.heroku.com/fastapi-singlestore-backend_app4/web
```

Push containers to docker hub:

```sh
docker push registry.heroku.com/app1/web
docker push registry.heroku.com/app2/web
docker push registry.heroku.com/app3/web
docker push registry.heroku.com/app4/web
docker push registry.heroku.com/lb/web
```

Deploy containers on Heroku:

```sh
heroku container:push app1 --app ${your heroku app}
heroku container:push app2 --app ${your heroku app}
heroku container:push app3 --app ${your heroku app}
heroku container:push app4 --app ${your heroku app}
heroku container:push lb --app ${your heroku app}
```

Todo: Figure out a better way to deploy multiple containers on Heroku because the above didn't work(it seems like it is not possible).

### Vercel (Not Possible)

This project makes use of WebSockets, which are unforunately not supported by Vercel's serverless functions.

[![Deploy on Vercel](https://camo.githubusercontent.com/f209ca5cc3af7dd930b6bfc55b3d7b6a5fde1aff/68747470733a2f2f76657263656c2e636f6d2f627574746f6e)](https://vercel.com/import/project?template=https://github.com/wiseaidev/fastapi-singlestore-backend)

### Netlify (Not Possible)

This project makes use of WebSockets, which are unforunately not supported by Netlify's serverless functions.

Additionally, running a FastAPI app is not possible on Netlify because the app consists of server side rendering. Only client side rendering is currently allowed on Netlify, which means that you can only deploy statically generated websites like docs and such. I tried to hack my way around it by creating a serverless function that executes `uvicorn main:app --reload` in the background. However, the serverless function is being deployed on a different environment.

[![Deploy on Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/wiseaidev/fastapi-singlestore-backend)

## Core Dependencies

The following packages are the main dependencies used to build this project:

- [`python`](https://github.com/python/cpython)
- [`fastapi`](https://github.com/tiangolo/fastapi)
- [`uvicorn`](https://github.com/encode/uvicorn)
- [`pydantic`](https://github.com/pydantic/pydantic)
- [`SQLAlchemy`](https://github.com/sqlalchemy/sqlalchemy)
- [`PyJWT`](https://github.com/jpadilla/pyjwt)
- [`passlib`](https://passlib.readthedocs.io/en/stable/index.html)
- [`aiomysql`](https://github.com/aio-libs/aiomysql)
- [`aioredis`](https://github.com/aio-libs/aioredis-py)
- [`python-multipart`](https://github.com/andrew-d/python-multipart)
- [`deta-python`](https://github.com/deta/deta-python)
- [`prometheus-fastapi-instrumentator`](https://github.com/trallnag/prometheus-fastapi-instrumentator)

## TODO and Contributions

This project is open for anyone to contribute:

- Adding support for multimedia messages other than images such as PDFs, txt, and more.
- Store messages content in the database as encrypted data rather than plain text. You can refer to the signal protocol for ideas.
- Sending voice messages.
- Design and implement a k8s architecture and deploy it on GCP.

## License

This project and the accompanying materials are made available under the terms and conditions of the [`MIT LICENSE`](https://github.com/wiseaidev/fastapi-singlestore-backend/blob/main/LICENSE).
