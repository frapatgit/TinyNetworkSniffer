FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY webserver /webserver

# Einrichten des Shared Folders
VOLUME /shared

CMD ["python", "flask_webserver.py"]