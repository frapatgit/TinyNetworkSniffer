import sqlite3
import json
import requests
import os


# Verbindung zur Datenbank erstellen oder vorhandene Verbindung öffnen
conn = sqlite3.connect('../webserver/database.db')
# Cursor-Objekt erstellen
cursor = conn.cursor()

# Tabelle erstellen, falls sie nicht vorhanden ist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dns_queries
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     timestamp TEXT,
     source_ip TEXT,
     destination_ip TEXT,
     protocol TEXT,
     dns_query TEXT,
     vt_score TEXT,
     vt_lastcheck TEXT)
''')

# Host-IP-Adresse festlegen
host = requests.get('https://ifconfig.me/ip').text.strip()

# Datei mit den DNS-Abfragen öffnen und zeilenweise auslesen
with open('targets.txt', 'r') as f:
    for line in f:
        # JSON-Daten aus der Zeile extrahieren
        data = json.loads(line)
        
        # Source-IP und Destination-IP auslesen
        src_ip = data['SourceIP']
        dst_ip = data['DestinationIP']
        
        # Überprüfen, ob Source-IP und Destination-IP leer sind
        if src_ip == '' or dst_ip == '':
            continue
        
        # Falls eine der IP-Adressen gleich der Host-IP-Adresse ist, 'router' eintragen
        if src_ip == host:
            src_ip = 'router'
        if dst_ip == host:
            dst_ip = 'router'
        
        # Überprüfen, ob die Daten bereits in der Datenbank vorhanden sind
        cursor.execute('SELECT COUNT(*) FROM dns_queries WHERE timestamp=? AND source_ip=? AND destination_ip=? AND protocol=? AND dns_query=?',
                       (data['Timestamp'], src_ip, dst_ip, data['Protocol'], data['DNSQuery']))
        if cursor.fetchone()[0] == 0:
            # Daten in die Datenbank einfügen
            cursor.execute('INSERT INTO dns_queries (timestamp, source_ip, destination_ip, protocol, dns_query) VALUES (?, ?, ?, ?, ?)',
                           (data['Timestamp'], src_ip, dst_ip, data['Protocol'], data['DNSQuery']))
        # Änderungen speichern
conn.commit()
        # Verbindung zur Datenbank schließen
conn.close()

def done():
    print("Daten erfolgreich in die Datenbank kopiert, starte löschen der targets.txt")
    os.remove("targets.txt")
    print("targets.txt gelöscht")

done()