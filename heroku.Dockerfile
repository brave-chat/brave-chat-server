# A workaround to run both the client and the server on heroku in one container.
FROM python:3.9.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install make and curl
RUN apt-get update \
 && apt-get install -y make curl --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Dependencies
COPY ./poetry.lock ./pyproject.toml ./Makefile ./
RUN make docker-install

COPY ./app ./app

# Client

ENV REACT_APP_SERVER_URL=http://0.0.0.0:8000/api/v1
ENV REACT_APP_SOCKET_URL=ws://0.0.0.0:8000/api/v1/ws

WORKDIR /client

# Install npm
RUN apt-get update \
 && apt install -y npm --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY ./brave-chat/package.json  ./
COPY ./brave-chat/src ./src
COPY ./brave-chat/public ./public

RUN npm install --force

# Run both server and client
COPY ./run.sh  ./
CMD ["sh", "./run.sh"]
