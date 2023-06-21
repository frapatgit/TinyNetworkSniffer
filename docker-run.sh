docker run -d \
    --name TinyNetworkSniffer \
    -p 5000:5000 \
    -v $(pwd)/webserver:/webserver \
    tns:latest
