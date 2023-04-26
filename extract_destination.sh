#!/bin/bash

dir="./captures"

# Schleife durch die Dateien im Verzeichnis /captures
latest_file=""
for file in $dir/capture_*.pcap; do
    if [ -z "$latest_file" ] || [ "$file" -nt "$latest_file" ]; then
        latest_file="$file"
    fi
done

pcap_file=$latest_file

domain_output="./destinations.txt"

# Filter-Optionen (ohne "not broadcast" und "not multicast")
filter="(ip or icmp or tcp or udp) and not arp"

# Mit tshark alle Quell-/Ziel-IP-Adressen und Domains extrahieren
tshark -r "$pcap_file" -T fields -e ip.src -e ip.dst -e http.host -e dns.qry.name -Y "$filter" | awk '{ if ($1 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) print $1; if ($2 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) print $2; if ($3 != "") print $3; if ($4 != "") print $4 }' | sort | uniq > "$domain_output"

# Nur Domains extrahieren
tshark -r "$pcap_file" -T fields -e dns.qry.name -Y "$filter" | sort | uniq >> "$domain_output"

# Ausgabe-Dateien anzeigen
echo "Quell-/Ziel-IP-Adressen wurden in $ip_output gespeichert:"
cat "$ip_output"
echo
echo "Domains wurden in $domain_output gespeichert:"
cat "$domain_output"
