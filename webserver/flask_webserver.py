from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    make_response,
    jsonify,
)
import sqlite3
import requests
import vt
import configparser


config = configparser.ConfigParser()

config.read("config.ini")
config.sections()
VT_API_KEY = config["credentials"]["API"]
app = Flask(__name__)
app.secret_key = "?rtl/S&O=@873@q(o!1t"


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/authenticate", methods=["POST"])
def authenticate():
    username = request.json["username"]
    password = request.json["password"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password)
    )
    user = c.fetchone()
    conn.close()
    if user:
        session["username"] = username
        response = make_response("OK", 200)
        return response
    else:
        return "Invalid username or password.", 401


@app.route("/logout")
def logout():
    session.pop("username", None)
    response = make_response(redirect(url_for("login")))
    response.set_cookie("session", "", expires=0)
    return response


@app.route("/home")
def home():
    if "username" in session:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT source_ip, destination_ip, vt_score FROM dns_queries LIMIT 10"
        )
        rows = c.fetchall()
        conn.close()
        return render_template("home.html", rows=rows)
    else:
        return redirect(url_for("login"))


@app.route("/settings")
def settings():
    if "username" in session:
        return render_template("settings.html")
    else:
        return redirect(url_for("login"))


@app.route("/queries")
def queries():
    if "username" in session:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT source_ip, destination_ip, timestamp, vt_score FROM dns_queries LIMIT 20"
        )
        rows = c.fetchall()
        conn.close()
        return render_template("queries.html", rows=rows)
    else:
        return redirect(url_for("login"))


@app.route("/clients")
def domains():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM dns_queries")
    domains = c.fetchall()
    conn.close()
    return render_template("clients.html", domains=domains)


@app.route("/check-url", methods=["POST"])
def check_url():

    client = vt.Client(VT_API_KEY)
    response = client.scan_url(request.args.get("url"))

    return jsonify(response.json())


if __name__ == "__main__":
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL);"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS dns_queries
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    source_ip TEXT,
                    destination_ip TEXT,
                    protocol TEXT,
                    dns_query TEXT,
                    vt_score TEXT);"""
    )

    conn.commit()
    conn.close()
    app.run("0.0.0.0", debug=True, port=5000)
