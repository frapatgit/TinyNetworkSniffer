import requests


# API Key einlesen
config_file = open('config.ini')
for line in config_file:
    line = line.strip()
    if line and line.startswith('API') :
        conf=line
config_file.close()
API= conf[5:-1]
print(API)
#set vt api v3
url = "https://www.virustotal.com/api/v3/urls"

#send post and get requests for urls

#loop through database here; adjust target variable
#send post to receive id
target = "android-cdn-api.fitbit.com"
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
#extract vt scores
harmlessscore = data["data"]["attributes"]["last_analysis_stats"]["harmless"]
maliciousscore = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
suspiciousscore = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]
undetectedscore = data["data"]["attributes"]["last_analysis_stats"]["undetected"]
print("harmlessscore: " + str(harmlessscore), "maliciousscore: "+ str(maliciousscore),"suspiciousscore: "+ str(suspiciousscore),"undetectedscore: "+ str(undetectedscore))

