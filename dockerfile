# Verwende ein ARM-basiertes CentOS-Image als Basis
FROM arm32v7/centos:latest

# Aktualisiere das System und installiere erforderliche Pakete
RUN yum -y update && yum -y install epel-release && yum -y install privoxy

# Kopiere die Privoxy-Konfigurationsdatei in das Image
COPY privoxy-config /etc/privoxy/config

# Öffne Port 8118 für den Privoxy-Proxy
EXPOSE 8118

# Starte Privoxy-Dienst beim Start des Containers
CMD ["/usr/sbin/privoxy", "--no-daemon"]
