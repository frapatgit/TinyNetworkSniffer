FROM python:3.9-alpine

WORKDIR /webserver

COPY requirements.txt requirements.txt
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo pkgconfig
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY webserver /webserver

# Einrichten des Shared Folders als Volumen
VOLUME /webserver

# Port für die Kommunikation mit dem Webserver freigeben
EXPOSE 5000

CMD ["python", "flask_webserver.py"]
