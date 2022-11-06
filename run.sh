#!/bin/sh

# turn on bash's job control
set -m

# cd into server
cd ../app

# Start the server and put it in the background
/root/.local/bin/poetry run server &

# cd into client
cd ../client

# Start the client
npm start
