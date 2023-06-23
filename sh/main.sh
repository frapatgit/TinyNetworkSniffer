#!/bin/env bash

TAG="[main_sh]"
# Handle user stoping the script.
trap 'pkill -f "wget|fritzdump";echo "$TAG exiting..."; exit' INT
## Debug option! Silentmode
# start fritzdump.sh in background and redirect its output to /dev/null
./fritzdump.sh >/dev/null 2>&1 &

# set the interval to 15 seconds
interval=10
scan_count=0
while true; do
    # wait for $interval seconds
    sleep $interval

    # check if fritzdump process is still running
    if ! pgrep fritzdump > /dev/null; then
        echo "$TAG fritzdump process is not running. Restarting..."

        # kill all wget and fritzdump processes
        pkill -f 'wget|fritzdump'

        # start fritzdump.sh in background
        ./fritzdump.sh &
    fi

    # start extract_destinations.sh and sync_db.py
    bash extract_destination.sh
    python sync_db.py
    python check_targets.py
    # erhöhe den count für den scan vorgang
    scan_count+=12
    #starte scan nur alle 30 minuten
    if [ $scan_count -ge 1800 ]
    then
        # starte scan für hosts
        python scan_network.py &
    fi

done