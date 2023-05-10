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
import configparser
import base64


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
        # Get remaining requests on vt
        api_url = f"https://www.virustotal.com/api/v3/users/{VT_API_KEY}/overall_quotas"
        headers = {
            "x-apikey": VT_API_KEY
        }
        response = requests.get(api_url, headers=headers)
        vt_quota = []
        vt_quota.append(["API requests this hour"] + list(response.json()["data"]["api_requests_hourly"]["user"].values()))
        vt_quota.append(["API requests today"] + list(response.json()["data"]["api_requests_daily"]["user"].values()))
        vt_quota.append(["API requests this month"] + list(response.json()["data"]["api_requests_monthly"]["user"].values()))
        return render_template("settings.html", vt_quota=vt_quota)
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
        print(rows)
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
    if "username" in session:
        url_id = base64.urlsafe_b64encode(request.json["url"].encode()).decode().strip("=")
        api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        app.logger.info(api_url)
        headers = {
            "accept": "application/json",
            "x-apikey": VT_API_KEY
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            return "Invalid url.", 400
        # @todo style output
        return jsonify(response.json()["data"]["attributes"]["total_votes"])
    else:
        return redirect(url_for("login"))


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
