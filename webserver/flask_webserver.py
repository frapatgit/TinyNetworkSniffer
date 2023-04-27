from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

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
        return "OK", 200
    else:
        return "Invalid username or password.", 401

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "username" in session:
        return render_template("home.html")
    else:
        return redirect(url_for("home"))

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
    #c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password"))
    #c.execute("INSERT INTO domains (domain_name) VALUES (?)", ("example.com",)) # Hier muss ein Tupel mit einem Element übergeben werden, um einen Fehler zu vermeiden.
    #c.execute("INSERT INTO ip_address (ip_address) VALUES (?)", ("192.168.10.1",)) # Hier muss ebenfalls ein Tupel mit einem Element übergeben werden.
    conn.commit()
    conn.close()
    app.run(debug=True)