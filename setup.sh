echo "[#] creating certificates for the webserver..."
cd webserver
mkdir cert
cd cert
openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout key.pem -out cert.pem -subj "/CN=TinyNetworkSniffer" -days 365
echo "[#] certs created"
cd ..
echo "[#] building docker"
cd ..
bash ./docker-build.sh
echo "[#] built docker "
echo "[#] starting docker-container"
bash ./docker-run.sh
echo "[#] webserver is ready"
echo "[#] starting monitoring"
bash ./sh/main.sh
echo "[#] monitoring started"
echo "[#] setup completed"