from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "?rtl/S&O=@873@q(o!1t"

@app.route("/")
def index():
    if "username" in session:
        return render_template("login.html")
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("example.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/domains")
def domains():
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute("SELECT * FROM domains")
    domains = c.fetchall()
    conn.close()
    return render_template("domains.html", domains=domains)

if __name__ == "__main__":
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS domains
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip_address TEXT NOT NULL,
                 domain_name TEXT NOT NULL);''')
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password"))
    c.execute("INSERT INTO domains (ip_address, domain_name) VALUES (?, ?)", ("192.168.1.1", "example.com"))
    conn.commit()
    conn.close()
    app.run(debug=True)