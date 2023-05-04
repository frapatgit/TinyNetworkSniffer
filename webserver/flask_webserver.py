from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
import sqlite3
import requests

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
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
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
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT domain_name, COUNT(*) FROM domains GROUP BY domain_name ORDER BY COUNT(*) DESC LIMIT 10')
        domains = c.fetchall()
        conn.close()
        return render_template('home.html', domains=domains)
    else:
        return redirect(url_for("login"))

@app.route("/settings")
def settings():
    if "username" in session:
        return render_template("settings.html")
    else:
        return redirect(url_for("settings"))

@app.route("/queries")
def queries():
    if "username" in session:
        return render_template("queries.html")
    else:
        return redirect(url_for("queries"))

@app.route("/clients")
def domains():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM domains")
    domains = c.fetchall()
    conn.close()
    return render_template("clients.html", domains=domains)
    
@app.route('/check-url', methods=['POST'])
def check_url():

    api_url = f'https://www.virustotal.com/api/v3/urls'
    api_key = '<your-api-key>'
    payload = f'url={request.json["url"]}'
    app.logger.info(payload)
    headers = {
        "accept": "application/json",
        "x-apikey": api_key,
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post(api_url, data=payload, headers=headers)
    app.logger.info(response.status_code)
    return jsonify(response.json())

if __name__ == "__main__":
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS domains
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 domain_name TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS ip_address
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip_address TEXT NOT NULL);''')


    conn.commit()
    conn.close()
    app.run("0.0.0.0", debug=True, port=5000)
