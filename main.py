# Entrypoint for Deta Micros
from sys import path

path.append(".")

from app.main import (
    chat_app,
)

app = chat_app
