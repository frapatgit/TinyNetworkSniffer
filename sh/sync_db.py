import sqlite3
import re

conn = sqlite3.connect('../webserver/database.db')
c = conn.cursor()

# Datei öffnen und Liste der Targets auslesen
with open('targets.txt') as f:
    target_list = f.read().splitlines()

# Filter IP from domains
domains = []
ips = []

ips = list(filter(lambda x: re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", x), target_list))
domains = target_list
for i in ips:
    if i in domains:
        domains.remove(i)

# daten in die datenbank schreiben
# ips in datenbank schreiben
for ip in ips:
    # Prüfen, ob die IP-Adresse bereits in der Datenbank existiert
    query = "SELECT ip_address FROM ip_address WHERE ip_address = ?"
    existing_ip = c.execute(query, (ip,)).fetchone()
    # Wenn die IP-Adresse noch nicht in der Datenbank existiert, füge sie hinzu
    if existing_ip is None:
        c.execute("INSERT INTO ip_address (ip_address) VALUES (?)", (ip,))

#domains in datenbank schreiben
for domain in domains:
    # Prüfen, ob die domain bereits in der Datenbank existiert
    query = "SELECT domain_name FROM domains WHERE domain_name = ?"
    existing_domain = c.execute(query, (domain,)).fetchone()
    # Wenn die domain noch nicht in der Datenbank existiert, füge sie hinzu
    if existing_domain is None:
        c.execute("INSERT INTO domains (domain_name) VALUES (?)", (domain,))
        
conn.commit()
conn.close()