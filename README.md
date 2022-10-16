# Chat App SingleStore Based Backend

A fully async based backend for the [chat application](github.com/wiseaidev/chat) built using FastAPI, SingleStore with aiomysql, [databases](https://github.com/encode/databases), pydantic, SQLAlchemy, and Deta.

## Development Requirements

- Python3.9
- Pip
- Poetry (Python Package Manager)

## Mysql Config

### 1. Configure mysql server on localhost

For mysql:

```sh
$ sudo apt-get update
$ sudo apt-get install mysql-server libmysqlclient-dev
$ sudo mysql_secure_installation
```

### 2. Configure the root user credentials

```sh
$ mysql -u root
> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
> FlUSH PRIVILEGES;
> exit;
```

## Installation

```sh
python -m venv .venv
source .venv/bin/activate
make install
```

## Runnning Localhost

`make run`

## Build app

`make up`

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8000/docs>

## Access Redocs Documentation

> <http://localhost:8000/redocs>

