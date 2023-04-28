#!/bin/bash

## Debug option! Silentmode
# start fritzdump.sh in background and redirect its output to /dev/null
./fritzdump.sh >/dev/null 2>&1 &

# set the interval to 15 seconds
interval=10

while true; do
    # wait for $interval seconds
    sleep $interval

    # check if fritzdump process is still running
    if ! pgrep fritzdump > /dev/null; then
        echo "fritzdump process is not running. Restarting..."

        # kill all wget and fritzdump processes
        pkill -f 'wget|fritzdump'

        # start fritzdump.sh in background
        ./fritzdump.sh &
    fi

    # start extract_destinations.sh and sync_db.py
    bash extract_destination.sh &
    python sync_db.py &
done