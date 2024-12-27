#!/bin/bash

set -o allexport
source .env
set +o allexport
TARGET_DIR="\${HOME}/tetris-m68k-server"
DOCKER_PREV_CTX=$(docker context show)
docker context use tetris-m68k

# setup folder structure if it does not exist
ssh tetris@tetris-m68k "[ -d '${TARGET_DIR}' ] || mkdir -p ${TARGET_DIR}"
ssh tetris@tetris-m68k "[ -d '${TARGET_DIR}/.venv' ] || python3 -m venv ${TARGET_DIR}/.venv"

# stop services
docker compose -f src/db/docker-compose.yml down

# deploy changes
rsync -avz -e "ssh" $PWD/start.sh $PWD/.env $PWD/src/server.py $PWD/requirements.txt tetris@tetris-m68k:${TARGET_DIR}/

# start services 
docker compose -f src/db/docker-compose.yml up -d --build
# ssh tetris@tetris-m68k "${TARGET_DIR}/start.sh"

# cleanup
docker context use ${DOCKER_PREV_CTX}
