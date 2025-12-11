#!/bin/bash
set -e; python3 update.py; [ ! -d echo-bot ] && exit 1; cd echo-bot; exec bash start.sh
