# Chat App SingleStore Based Backend

A fully async based backend for the [chat application](https://github.com/wiseaidev/chat) built using FastAPI, SingleStore with aiomysql, [databases](https://github.com/encode/databases), pydantic, SQLAlchemy, and Deta.

## Development Requirements

- Python3.9
- Pip
- Poetry (Python Package Manager)


## Installation with make

```sh
$ make
Please use 'make <target>' where <target> is one of:

install                  Install the package and all required core dependencies
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

### 5. Run the server

Fill in the following variables in your .env file accordingly:

```yaml
# Database
SINGLESTORE_USERNAME=admin
SINGLESTORE_PASSWORD=<database password>
SINGLESTORE_HOST=<database name>
SINGLESTORE_PORT=3306
SINGLESTORE_DATABASE=<database name>
```

### 6. Generate a secret key

Generate a secret key using openssl and update it env var in .env file.

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
