FROM python:3.9-slim-buster

WORKDIR /webserver

COPY requirements.txt requirements.txt
COPY sh/config.ini config.ini
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY webserver /webserver

# Einrichten des Shared Folders
VOLUME /shared

# Port für die Kommunikation mit dem Webserver freigeben
EXPOSE 5000

CMD ["python", "flask_webserver.py"]
