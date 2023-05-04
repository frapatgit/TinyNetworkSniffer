import requests
import configparser
import json

# API Key einlesen
config = configparser.ConfigParser()
config.read('config.ini')
API = config.get('virustotal', 'API')[1:-1]
#set vt api v3
url = "https://www.virustotal.com/api/v3/urls"

#send post and get requests for urls

#loop through database here; adjust target variable
#send post to receive id
target = "google.de"
payload = "url="+target

headers = {
    "accept": "application/json",
    "x-apikey": API,
    "content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)
data = response.json()
id_value = data["data"]["id"][2:-11]
print(id_value)

#send get to receive vt scores
url2 = url+"/"+id_value
print(url2)
headers = {
    "accept": "application/json",
    "x-apikey": API
}
response = requests.get(url2, headers=headers)
data = response.json()
harmlessscore = data["data"]["attributes"]["last_analysis_stats"]["harmless"]
maliciousscore = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
suspiciousscore = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]
undetectedscore = data["data"]["attributes"]["last_analysis_stats"]["undetected"]
print("harmlessscore: " + str(harmlessscore), "maliciousscore: "+ str(maliciousscore),"suspiciousscore: "+ str(suspiciousscore),"undetectedscore: "+ str(undetectedscore))


#extract vt scores