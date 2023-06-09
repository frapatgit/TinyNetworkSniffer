#!/bin/bash

## Data in targets.txt has the following format:
##Packet1{
#Timestamp: "Timestamp",
#SourceIP:"SourceIP",
#DestinationIP:"DestinationIP",
#DNSQuery:"DNSQuery",
#TotalCount:"Count"
#}
##
TAG="[extract_destination]"

dir="./captures"

# Schleife durch die Dateien
while true; do
  latest_file="$(ls -t "$dir" | head -n1)"
  if [[ -n "$latest_file" ]]; then
    if [[ $(stat -c%s "$dir/$latest_file") -eq 0 ]]; then
      rm "$dir/$latest_file"
      echo "$TAG### Die Datei $latest_file wurde gelöscht."
    else
      echo "$TAG### Die neueste Datei ist größer als 0 Byte."
      break
    fi
  else
    echo "$TAG### Keine Dateien im Verzeichnis gefunden."
    break
  fi
done

pcap_file="$dir/$latest_file"

domain_output="./targets.txt"

# Filter-Optionen (ohne "not broadcast" und "not multicast")
filter="(ip or icmp or tcp or udp) and not arp"

# Mit tshark alle Quell-/Ziel-IP-Adressen und Domains extrahieren
tshark -r "$pcap_file" -T fields -E separator=\; -e frame.time_epoch -e ip.src -e ip.dst -e http.host -e dns.qry.name -e _ws.col.Protocol -Y "$filter" | awk -F ";" '{
    if ($2 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) {
        src=$2;
        dst=$3
    } else {
        src=$3;
        dst=$4
    };
    if ($5 != "") {
        printf("{\"Timestamp\":\"%s\",\"SourceIP\":\"%s\",\"DestinationIP\":\"%s\",\"Protocol\":\"%s\",\"DNSQuery\":\"%s\"}\n", strftime("%Y-%m-%d %H:%M:%S", $1), src, dst, $6, $5)
    } else {
        printf("{\"Timestamp\":\"%s\",\"SourceIP\":\"%s\",\"DestinationIP\":\"%s\",\"Protocol\":\"%s\",\"DNSQuery\":\"%s\"}\n", strftime("%Y-%m-%d %H:%M:%S", $1), src, dst, $6, $7)
    }
}' >> "$domain_output"


# Ausgabe-Dateien anzeigen
echo "----------------------------------"
echo "$TAG### Domains wurden in $domain_output gespeichert:"
#cat "$domain_output"
echo "----------------------------------"

## Duplikate aus destinations.txt entfernen
input_file=$domain_output

# Prüfen, ob die Eingabedatei existiert
if [ ! -f "$input_file" ]; then
    echo "$TAG### Eingabedatei $input_file existiert nicht."
    exit 1
fi

# Duplikate entfernen
sort -u -o "$input_file" "$input_file"

echo "$TAG### Duplikate erfolgreich aus $input_file entfernt."

# Fehlerbehandlung - Prüfen, ob die Datei existiert
if [ -e "$file_to_delete" ]; then
    # Datei löschen
    rm "$file_to_delete"
    echo "$TAG### Datei $file_to_delete erfolgreich gelöscht."
else
    echo "$TAG### Datei $file_to_delete existiert nicht."
fi