import sqlite3
import nmap
import netifaces
import ipaddress
import socket

def get_network_cidr():
    gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    addrs = netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])
    netmask = addrs[netifaces.AF_INET][0]['netmask']
    ip_net = ipaddress.ip_network(f"{gateway}/{netmask}", strict=False)
    return str(ip_net)

def get_hostnames(ip_addresses):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_addresses, arguments="-sL -n")
    hosts = nm.all_hosts()
    hostnames = [nm[host].hostname() for host in hosts if 'hostname' in nm[host]]
    return hostnames

def scan_network():
    # Erstellen einer Verbindung zur Datenbank
    conn = sqlite3.connect('../webserver/database.db')
    cursor = conn.cursor()

    # Erstellen einer neuen Tabelle für Hosts, wenn sie noch nicht existiert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            hostname TEXT,
            status TEXT
        )
    ''')

    # IP-Adresse des Standardgateways finden
    subnet = get_network_cidr()
    print("Subnetzmaske gefunden: "+subnet )
    # Scannen des Netzwerks mit nmap
    print("Starte scanning der aktiven hosts.." )
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-sn')
    # Löschen aller Einträge aus der Tabelle 'hosts'
    cursor.execute('DELETE FROM hosts')

    # Durchlaufen der Ergebnisse und Einfügen in die Tabelle
    for host in nm.all_hosts():
        ip_address = host
        hostname = socket.getfqdn(ip_address)
        status = nm[host].state()
        cursor.execute('INSERT INTO hosts (ip_address, hostname, status) VALUES (?, ?, ?)',
                       (ip_address, hostname, status))
        

    # Speichern der Änderungen und Schließen der Verbindung zur Datenbank
    conn.commit()
    conn.close()

scan_network()