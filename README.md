
# Tiny Network Sniffer


### für Advanced Programming SS 2023

Patrick Frank und Johannes Reusch.



## Epic:

Als Netzwerkadministrator möchte ich einen Docker-Container erstellen, der den Netzwerktraffic auf einem Gerät im Netzwerk per tcpdump mitschneidet und die Domains mit Hilfe von VirusTotal überprüft. Die als bösartig markierten Domains sollen an einen Webserver gesendet werden. Auf diesem Webserver möchte ich mich anmelden und Statistiken zu den bösartigen Domains anzeigen lassen können. Der Datenaustausch zwischen dem Docker-Container und dem Webserver soll verschlüsselt stattfinden, um die Daten vor unautorisiertem Zugriff zu schützen.

## User-Storys:

User-Story 1:
Als Netzwerkadministrator möchte ich einen Docker-Container erstellen, der den Netzwerktraffic auf einem Gerät im Netzwerk mitschneidet.

User-Story 2: 
Als Netzwerkadministrator möchte das alle Domains die innerhalb des Netwerkes aufgerufen wurden abgespeichert werden und abgerufen werden können.

User-Story 3:
Als Netzwerkadministrator möchte ich den Netzwerktraffic mit VirusTotal überprüfen und bösartige Domains identifizieren, wobei der Datenaustausch zwischen dem Docker-Container und dem Webserver verschlüsselt stattfindet.

User-Story 4:
Als Netzwerkadministrator möchte ich, dass der Docker-Container bösartige Domains an einen Webserver sendet und dass dieser Datenaustausch verschlüsselt stattfindet.

User-Story 5:
Als Netzwerkadministrator möchte ich mich auf dem Webserver anmelden können und Statistiken zu den bösartigen Domains auf dem Webserver anzeigen lassen. Der Datenaustausch zwischen dem Docker-Container und dem Webserver soll verschlüsselt stattfindet.
