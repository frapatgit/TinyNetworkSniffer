
# Tiny Network Sniffer


### für Advanced Programming SS 2023

Patrick Franck und Johannes Reusch.



## Epic:

Als Netzwerkadministrator möchte ich einen Docker-Container erstellen, der den Netzwerktraffic auf einem Gerät im Netzwerk per tcpdump mitschneidet und die Domains mit Hilfe von VirusTotal überprüft. Die als bösartig markierten Domains sollen an einen Webserver gesendet werden. Auf diesem Webserver möchte ich mich anmelden und Statistiken zu den bösartigen Domains anzeigen lassen können. Der Datenaustausch zwischen dem Docker-Container und dem Webserver soll verschlüsselt stattfinden, um die Daten vor unautorisiertem Zugriff zu schützen.

## User-Storys:

User-Story 1: Als Netzwerkadministrator möchte ich einen Docker-Container erstellen, der den Netzwerktraffic auf einem Gerät im Netzwerk per tcpdump mitschneidet und den Datenaustausch zwischen dem Docker-Container und dem Webserver verschlüsselt.

User-Story 2: Als Netzwerkadministrator möchte ich eine Liste an gefährlichen Websites über eine Oberfläche zugänglich haben um Sie Nutzern zeigen zu können und damit zu warnen.

User-Story 3: Als IT-Sec Enthusiast möchte ich mit tcpdump den Verkehr im Netzwerk überwachen und nach auffälligen Websites untersuchen, dies möchte Ich jederzeit über eine GUI abrufen können.

User-Story 4: Als Programmierer möchte ich mich einen Dienst der mir alle auffälligen Webseiten die im Netzwerk aufgerufen werden liefert damit Ich sie programmatisch abrufen kann.

User-Story 5: Als Internetnutzer möchte ich einfach sehen ob in meinem Netzwerk gefährliche Webseiten aufgerufen werden und dies über eine Weboberfläche abrufen.



