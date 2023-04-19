#!/bin/bash
# usage program.sh <filename.pcap>

tshark -r "$1" -T fields -e ip.src -e dns.qry.name -2R "dns.flags.response eq 0" | awk -F" " '{ print $2 }' | sort -u
