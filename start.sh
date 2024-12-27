#!/bin/bash
source ${HOME}/tetris-m68k-server/.venv/bin/activate
pip install -r ${HOME}/tetris-m68k-server/requirements.txt
kill -9 $(cat ${HOME}/tetris-m68k-server/server.pid)
# TODO: server.log doesn't show anything
${HOME}/tetris-m68k-server/server.py >> ${HOME}/tetris-m68k-server/server.log 2>&1 & echo $! > ${HOME}/tetris-m68k-server/server.pid
