#!/bin/bash

dir="./captures"

# Schleife durch die Dateien
while true; do
  latest_file="$(ls -t "$dir" | head -n1)"
  if [[ -n "$latest_file" ]]; then
    if [[ $(stat -c%s "$dir/$latest_file") -eq 0 ]]; then
      rm "$dir/$latest_file"
      echo "### Die Datei $latest_file wurde gelöscht."
    else
      echo "### Die neueste Datei ist größer als 0 Byte."
      break
    fi
  else
    echo "### Keine Dateien im Verzeichnis gefunden."
    break
  fi
done

pcap_file="$dir/$latest_file"

domain_output="./targets.txt"

# Filter-Optionen (ohne "not broadcast" und "not multicast")
filter="(ip or icmp or tcp or udp) and not arp"

# Mit tshark alle Quell-/Ziel-IP-Adressen und Domains extrahieren
tshark -r "$pcap_file" -T fields -e ip.src -e ip.dst -e http.host -e dns.qry.name -Y "$filter" | awk '{ if ($1 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) print $1; if ($2 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) print $2; if ($3 != "") print $3; if ($4 != "") print $4 }' | sort | uniq >> "$domain_output"

# Nur Domains extrahieren
tshark -r "$pcap_file" -T fields -e dns.qry.name -Y "$filter" | sort | uniq >> "$domain_output"

# Ausgabe-Dateien anzeigen
echo "----------------------------------"
echo "### Domains wurden in $domain_output gespeichert:"
cat "$domain_output"
echo "----------------------------------"

## Duplikate aus destinations.txt entfernen
input_file=$domain_output

# Prüfen, ob die Eingabedatei existiert
if [ ! -f "$input_file" ]; then
    echo "### Eingabedatei $input_file existiert nicht."
    exit 1
fi

# Duplikate entfernen
sort -u -o "$input_file" "$input_file"

echo "### Duplikate erfolgreich aus $input_file entfernt."


file_to_delete=$pcap_file

# Fehlerbehandlung - Prüfen, ob die Datei existiert
if [ -e "$file_to_delete" ]; then
    # Datei löschen
    rm "$file_to_delete"
    echo "### Datei $file_to_delete erfolgreich gelöscht."
else
    echo "### Datei $file_to_delete existiert nicht."
fi
