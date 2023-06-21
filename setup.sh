cd sh
if [ ! -e "config.ini" ]; then
        touch config.ini
        echo "# Credentials for fritzbox and VirusTotal API" >> config.ini
        echo "# adjust accordingly" >> config.ini
        echo "[credentials]" >> config.ini
        clear
        echo "setup credentials for Virustotal API and Fritzbox:"
        read -p "Fritzbox username: " userInput
        echo "username=$userInput" >> config.ini
        read -p "Fritzbox passwort: " userInput
        echo "password=$userInput" >> config.ini
        read -p "Virustotal API Key: " userInput
        echo "API=$userInput" >> config.ini
fi
cd ..
cd webserver
if [ ! -d "cert" ]; then
        echo "[#] creating certificates for the webserver..."
        mkdir cert
        cd cert
        openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout key.pem -out cert.pem -subj "/CN=TinyNetworkSniffer" -days 365
        cd ..
        echo "[#] certs created"
fi
#create user for login
# Pfad zur SQLite-Datenbankdatei
DB_FILE="database.db"
# SQL-Befehl zum Einfügen eines Benutzers in die Tabelle "users"
INSERT_SQL="INSERT INTO users (username, password) VALUES ('$1', '$2');"

# Überprüfen, ob Benutzername und Passwort als Argumente übergeben wurden
if [ $# -ne 2 ]; then
  echo "Bitte geben Sie einen Benutzernamen und ein Passwort als Argumente an."
  exit 1
fi

# Eintrag hinzufügen
sqlite3 "$DB_FILE" "$INSERT_SQL"
#
cd ..
echo "[#] building docker"
bash docker-build.sh
echo "[#] built docker "
echo "[#] starting docker-container"
bash docker-run.sh
echo "[#] webserver is ready"
echo "[#] starting monitoring"
cd ./sh
chmod +x fritzdump.sh scan_network.py sync_db.py main.sh extract_destination.sh check_targets.py
bash main.sh
echo "[#] monitoring started"
echo "[#] setup completed"
