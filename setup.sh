cd sh
if [ ! -e "config.ini" ]; then
        echo "# Credentials for fritzbox and VirusTotal API" >> .sh/config.ini
        echo "# adjust accordingly" >> .sh/config.ini
        echo "[credentials]" >> .sh/config
        clear
        echo "setup credentials for Virustotal API and Fritzbox:"
        read -p "Fritzbox username: " userInput
        echo "$userInput" >> sh/config.ini
        read -p "Fritzbox passwort: " userInput
        echo "$userInput" >> sh/config.ini
        read -p "Virustotal API Key: " userInput
        echo "$userInput" >> sh/config.ini
fi
cd ..
cd webserver
if [ ! -d "cert" ]; then
        echo "[#] creating certificates for the webserver..."
        mkdir cert
        cd cert
        openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout key.pem -out cert.pem -subj "/CN=TinyNetworkSniffer" -days 365
        echo "[#] certs created"
fi
cd ..
echo "[#] building docker"
bash docker-build.sh
echo "[#] built docker "
echo "[#] starting docker-container"
bash docker-run.sh
echo "[#] webserver is ready"
echo "[#] starting monitoring"
cd ./sh
bash nohup main.sh &
echo "[#] monitoring started"
echo "[#] setup completed"
