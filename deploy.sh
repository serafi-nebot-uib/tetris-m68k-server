#!/bin/bash

# deploy changes to server (tetris-m68k.westeurope.cloudapp.azure.com)
rsync -avz -e "ssh" \
	--exclude=".mypy_cache" \
	--exclude="__pycache__" \
	--exclude="db" \
	$PWD/src/* tetris@tetris-m68k:/home/tetris/tetris-m68k-server/

# restart docker containers
cd src/db/
DOCKER_PREV_CTX=$(docker context show)
docker context use tetris-m68k
docker compose down
docker compose up -d --build
docker context use ${DOCKER_PREV_CTX}
unset DOCKER_PREV_CTX
cd -
