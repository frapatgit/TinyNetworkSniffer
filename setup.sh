#Dependency check
# Überprüfen, ob das Paket "sqlite3" bereits installiert ist
if ! command -v sqlite3 &> /dev/null; then
  echo "sqlite3 installation missing. installing now..."
  
  # Paketinstallation je nach Linux-Distribution
  if [[ -f /etc/debian_version ]]; then
    sudo apt-get update
    sudo apt-get install sqlite3
  else
    echo "[!] unknown OS. Please install sqlite3 manually"
    exit 1
  fi
  echo "[#] sqlite3 successful installed"
else
  echo "[#] sqlite3 is already installed"
fi
# Überprüfen, ob das Paket "python-nmap" bereits installiert ist
if pip3 show python-nmap >/dev/null 2>&1; then
  echo "[#] python-nmap already installed"
else
  echo "[#] installing python-nmap..."
  pip3 install python-nmap
fi
# Überprüfen, ob das Paket "netifaces" bereits installiert ist
if pip show netifaces >/dev/null 2>&1; then
  echo "[#] netifaces already installed"
else
  echo "[#] installing netifaces..."
  pip install netifaces
fi
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
#create db
# SQLite-Datenbank erstellen und zur Datenbank wechseln
sqlite3 database.db <<EOF
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
EOF

echo "Die Datenbank database.db wurde erfolgreich erstellt."
#create user for login
# Pfad zur SQLite-Datenbankdatei
DB_FILE="database.db"
# Benutzernamen und Passwort abfragen
read -p "Benutzername: " username
read -p "Passwort: " -s password
# SQL-Befehl zum Einfügen eines Benutzers in die Tabelle "users"
INSERT_SQL="INSERT INTO users (username, password) VALUES ('$username', '$password');"
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
