import sqlite3
import requests
import time
import configparser
import base64


# API Key einlesen
config_file = configparser.ConfigParser()
config_file.read("config.ini")

API= config_file["credentials"]["API"]
#set vt api v3
#send post and get requests for urls

#send post to receive id
def checkurl(target):
    target = base64.urlsafe_b64encode(target.encode()).decode().strip("=")
    url = "https://www.virustotal.com/api/v3/urls"
    payload = url + target
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
    table_name = "dns_queries"
    conn = sqlite3.connect('../webserver/database.db')
    c = conn.cursor()

    # Hole alle Einträge aus der Tabelle
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()

    # Für jeden Eintrag
    for row in rows:
        dns_query = row[5]
        vt_score = row[6]

        # Überprüfe, ob das dns_query Feld und das vt_score Feld nicht NULL sind
        if dns_query != "" and vt_score is None:
            # Gib das dns_query Feld aus
            vt_score = checkurl(dns_query)
            # Update den vt_score für den aktuellen Eintrag
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Aktueller Zeitstempel
            c.execute(f"UPDATE {table_name} SET vt_score = ?, vt_lastcheck = ? WHERE id = ?", (vt_score, current_time, row[0]))

    conn.commit()
    conn.close()

def update_vt_score_ips():
    table_name = "dns_queries"
    host =  requests.get('https://ifconfig.me/ip').text.strip()
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
            if source_ip == host:
                vt_score = checkip(destination_ip)
                if vt_score == "0/0":
                    vt_score="unrated"
            elif destination_ip == host:
                vt_score = checkip(source_ip)
                if vt_score == "0/0":
                    vt_score="unrated"
            # Aktualisiere den Eintrag in der Datenbank mit vt_score und dem aktuellen Zeitstempel
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            c.execute(f"UPDATE {table_name} SET vt_score = ?, vt_lastcheck = ? WHERE id = ?", (vt_score, current_time, row[0]))
    conn.commit()
    conn.close()

update_vt_score_domains()
update_vt_score_ips()