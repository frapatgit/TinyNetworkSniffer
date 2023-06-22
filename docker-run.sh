docker run -d \
    --name TinyNetworkSniffer \
    -p 5000:5000 \
    -v $(pwd)/webserver:/webserver \
    -v $(pwd)/sh/config.ini:/webserver/config.ini \
    tns:latest
