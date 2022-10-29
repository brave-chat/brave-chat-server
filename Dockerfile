FROM python:3.9.10-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# Install make and curl
RUN apt update && apt install -y make curl

# Install Dependencies
COPY poetry.lock pyproject.toml Makefile ./
RUN make docker-install

COPY ./app ./app
CMD ["/root/.local/bin/poetry", "run", "server"]
