import sqlite3
import requests
import time
import configparser
import re


# API Key einlesen
config_file = configparser.ConfigParser()
config_file.read("config.ini")
API= config_file["credentials"]["API"]
#set vt api v3
#send post and get requests for urls

#send post to receive id
def checkurl(target):
    url = "https://www.virustotal.com/api/v3/urls"
    payload = "url="+target
    headers = {
        "accept": "application/json",
        "x-apikey": API,
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    data = response.json()
    id_value = data["data"]["id"][2:-11]
    #send get to receive vt scores
    url2 = url+"/"+id_value
    headers = {
        "accept": "application/json",
        "x-apikey": API
    }
    response = requests.get(url2, headers=headers)
    data = response.json()
    #extract vt scores
    harmlessscore = data["data"]["attributes"]["last_analysis_stats"]["harmless"]
    maliciousscore = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
    suspiciousscore = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]
    undetectedscore = data["data"]["attributes"]["last_analysis_stats"]["undetected"]
    print("harmlessscore: " + str(harmlessscore), "maliciousscore: "+ str(maliciousscore),"suspiciousscore: "+ str(suspiciousscore),"undetectedscore: "+ str(undetectedscore))
    vt_scoretotal= str(maliciousscore + suspiciousscore) + "/" + str(harmlessscore + maliciousscore + suspiciousscore)
    return vt_scoretotal

def checkip(ip):
    vt = "https://www.virustotal.com/api/v3/ip_addresses/"
    url = vt + str(ip)
    headers = {
        "accept": "application/json",
        "x-apikey": API
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    #extract vt scores
    harmlessscore = data["data"]["attributes"]["last_analysis_stats"]["harmless"]
    maliciousscore = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
    suspiciousscore = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]
    undetectedscore = data["data"]["attributes"]["last_analysis_stats"]["undetected"]
    print("harmlessscore: " + str(harmlessscore), "maliciousscore: "+ str(maliciousscore),"suspiciousscore: "+ str(suspiciousscore),"undetectedscore: "+ str(undetectedscore))
    vt_scoretotal= str(maliciousscore + suspiciousscore) + "/" + str(harmlessscore + maliciousscore + suspiciousscore)
    return vt_scoretotal

#loop through database here
#updates vt score for dns requests
def update_vt_score_domains():
    table_name = "destinations"
    conn = sqlite3.connect('../webserver/database.db')
    c = conn.cursor()

    # Hole alle Einträge aus der Tabelle
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()

    # Für jeden Eintrag
    for row in rows:
        destination = row[0]
        vt_score = row[2]

        # Überprüfe, ob das dns_query Feld und das vt_score Feld nicht NULL sind
        if is_ipv4_address(destination) == True and vt_score is None:
            # Gib das dns_query Feld aus
            vt_score = checkurl(destination)
            # Update den vt_score für den aktuellen Eintrag
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Aktueller Zeitstempel
            c.execute(f"UPDATE {table_name} SET vt_score = ?, vt_lastcheck = ? WHERE id = ?", (vt_score, current_time, row[0]))

    conn.commit()
    conn.close()

def update_vt_score_ips():
    table_name = "dns_queries"
    conn = sqlite3.connect('../webserver/database.db')
    c = conn.cursor()

    # Hole alle Einträge aus der Tabelle
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()

    # Für jeden Eintrag
    for row in rows:
        source_ip = row[2]
        destination_ip = row[3]
        vt_score = row[6]
        vt_lastcheck = row[7]

        # Überprüfe, ob das vt_score und vt_lastcheck Feld NULL ist und die source_ip oder destination_ip nicht die Host-IP ist
        if vt_score is None:
            # Rufe checkip auf und speichere das Ergebnis in vt_score
            if source_ip == "router":
                vt_score = checkip(destination_ip)
                if vt_score == "0/0":
                    vt_score="unrated"
            elif destination_ip == "router":
                vt_score = checkip(source_ip)
                if vt_score == "0/0":
                    vt_score="unrated"
            # Aktualisiere den Eintrag in der Datenbank mit vt_score und dem aktuellen Zeitstempel
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            c.execute(f"UPDATE {table_name} SET vt_score = ?, vt_lastcheck = ? WHERE id = ?", (vt_score, current_time, row[0]))
    conn.commit()
    conn.close()

def create_destinations_table():
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect('../webserver/database.db')
    c = conn.cursor()

    # Neue Tabelle 'destinations' erstellen
    c.execute('''CREATE TABLE IF NOT EXISTS destinations 
                (destination TEXT, count INTEGER DEFAULT 1, vt_score INTEGER, vt_lastcheck TEXT, 
                 PRIMARY KEY (destination))''')

    # Daten aus 'dns_queries' Tabelle extrahieren
    c.execute('''SELECT source_ip, destination_ip, dns_query, vt_score, vt_lastcheck 
                FROM dns_queries''')

    # Alle Einträge durchgehen und in die 'destinations' Tabelle einfügen
    for row in c.fetchall():
        source_ip, destination_ip, dns_query, vt_score, vt_lastcheck = row

        # Nur Einträge mit 'router' in source_ip oder destination_ip berücksichtigen
        if source_ip == 'router':
            destination = destination_ip
        elif destination_ip == 'router':
            destination = source_ip
        else:
            continue  # Eintrag ohne 'router' ignorieren

        # Eintrag in 'destinations' Tabelle einfügen
        c.execute('''INSERT OR IGNORE INTO destinations (destination, vt_score, vt_lastcheck) 
                    VALUES (?, ?, ?)''',
                  (destination, vt_score, vt_lastcheck))

        # count um 1 erhöhen
        c.execute('''UPDATE destinations SET count = count + 1 WHERE destination=?''',
                  (destination,))

        # dns_query in 'destinations' Tabelle einfügen, wenn noch nicht vorhanden
        c.execute('''INSERT OR IGNORE INTO destinations (destination, vt_score, vt_lastcheck) 
                    VALUES (?, ?, ?)''',
                  (dns_query,None, None))
                # count um 1 erhöhen
        c.execute('''UPDATE destinations SET count = count + 1 WHERE destination=?''',
                  (dns_query,))
        c.execute('''DELETE FROM destinations WHERE destination='' ''')
    
    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

def is_ipv4_address(address):
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return bool(pattern.match(address))
    
def killthequota():
        api_url = f"https://www.virustotal.com/api/v3/users/{API}/overall_quotas"
        headers = {
            "x-apikey": API
        }
        response = requests.get(api_url, headers=headers)
        vt_quota_today = list(response.json()["data"]["api_requests_daily"]["user"].values())
        vt_quota_month= list(response.json()["data"]["api_requests_monthly"]["user"].values())
        print(vt_quota_today,vt_quota_month)
        if vt_quota_today[0] < vt_quota_today[1] and vt_quota_month[0] < vt_quota_month[1]:
            update_vt_scores()
            update_possible= True
        else:
            update_possible= False
        print(update_possible)

def update_vt_scores():
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect('../webserver/database.db')
    c = conn.cursor()

    # SQL-Abfrage ausführen
    c.execute('''SELECT * FROM destinations ORDER BY vt_lastcheck ASC LIMIT 10''')

    for row in c.fetchall():
        destination, count, vt_score, vt_lastcheck = row
        print(destination)
        if is_ipv4_address(destination) == True:
            vt_score = checkip(destination)
        else:
            vt_score = checkurl(destination)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        c.execute(f"UPDATE destinations SET vt_score = ?, vt_lastcheck = ? WHERE destination = ?", (vt_score, current_time, destination))

    # Verbindung schließen
    conn.commit()
    conn.close()

update_vt_score_domains()
update_vt_score_ips()
create_destinations_table()
killthequota()