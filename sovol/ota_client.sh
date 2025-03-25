#!/bin/bash

pids=($(pgrep -f ota_service.sh))
PID=${pids[1]}

if [ -z "$PID" ]; then
    exit 1
fi

kill -SIGUSR1 "$PID"
