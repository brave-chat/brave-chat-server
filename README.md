# Chat App SingleStore Based Backend

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/wiseaidev/fastapi-singlestore-backend/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/wiseaidev/fastapi-singlestore-backend/tree/main)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/wiseaidev/fastapi-singlestore-backend/main.svg)](https://results.pre-commit.ci/latest/github/wiseaidev/fastapi-singlestore-backend/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Banner](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rvoa7yq0f1grhumd6s0r.png)](https://github.com/wiseaidev/fastapi-singlestore-backend)

A fully async based backend for the [chat application](https://github.com/wiseaidev/chat) built using FastAPI, SingleStore with aiomysql, [databases](https://github.com/encode/databases), pydantic, SQLAlchemy, and Deta.

## Development Requirements

- Python (3.9)
- Poetry (1.2.2)

## Installation with make

```sh
$ make
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
$ make venv
```

### 2. Activate the virtualenv

```sh
$ source .venv/bin/activate
```

### 3. Install dependencies

```sh
$ make install
```

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

### 6. Generate a secret key

Generate a secret key using openssl and update its env var in .env file.

```sh
$ openssl rand -hex 128
afa1639545d53ecf83c9f8acf4704abe1382f9a9dbf76d2fd229d4795a4748712dbfe7cf1f0a812f1c0fad2d47c8343cd1017b22fc3bf43d052307137f6ba68cd2cb69748b561df846873a6257e3569d6307a7e022b82b79cb3d6e0fee00553d80913c1dcf946e2e91e1dfcbba1ed9f34c9250597c1f70f572744e91c68cbe76
```

```yaml
# App config:
JWT_SECRET_KEY=afa1639545d53ecf83c9f8acf4704abe1382f9a9dbf76d2fd229d4795a4748712dbfe7cf1f0a812f1c0fad2d47c8343cd1017b22fc3bf43d052307137f6ba68cd2cb69748b561df846873a6257e3569d6307a7e022b82b79cb3d6e0fee00553d80913c1dcf946e2e91e1dfcbba1ed9f34c9250597c1f70f572744e91c68cbe76
DEBUG=False
```

### 7. Run Localhost

```sh
$ make run
```

## Access Swagger Documentation

> <http://localhost:8000/docs>

## Access Redocs Documentation

> <http://localhost:8000/redocs>

## Deployment

To use the deta version of the API you'll need to create a Deta account.

### Deta Micros

This deployment option fits within the Deta theme.

[![Deploy on Deta](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/wiseaidev/fastapi-singlestore-backend)

### Using The CLI with make

Make sure you have Deta cli on your machine. If it is not the case, just run the following command(on a linux distro or Mac):

```sh
curl -fsSL https://get.deta.dev/cli.sh | sh
```

Manually add `/home/<user_name>/.deta/bin/deta` to your path:

```sh
PATH="/home/<user_name>/.deta/bin:$PATH"
```

Now you can deploy the app on a Deta Micro:

```sh
$ make deploy-deta
```

You can then use the Deta UI to check the logs and the URL the API is hosted on.

_NOTE: Make sure your `.env` file is filled with valid env vars values accordingly._

_NOTE: The `main.py` file is used as an entry point for deta. Same goes for `requirements.txt`._

_NOTE: Deta Micros are limited to 512MB per deployment._

### Heroku

[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wiseaidev/fastapi-singlestore-backend)

### Vercel

[![Deploy on Vercel](https://camo.githubusercontent.com/f209ca5cc3af7dd930b6bfc55b3d7b6a5fde1aff/68747470733a2f2f76657263656c2e636f6d2f627574746f6e)](https://vercel.com/import/project?template=https://github.com/wiseaidev/fastapi-singlestore-backend&env=JWT_SECRET_KEY,SINGLESTORE_USERNAME,SINGLESTORE_PASSWORD,SINGLESTORE_HOST,SINGLESTORE_PORT,SINGLESTORE_DATABASE&envDescription=Your%20SingleStoreDB%20Account%2C%20Credentials%20%20and%20JWT_SECRET_KEY%20ID%20)
