docker run -d \
    --name TinyNetworkSniffer \
    -p 5000:5000 \
    -v /home/pi/dockertests/TinyNetworkSniffer/sh:/shared \
    tns:latest