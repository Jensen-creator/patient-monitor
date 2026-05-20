from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# -------------------------
# DATABASE SETUP
# -------------------------
def init_db():
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS vitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            spo2 INTEGER,
            rr INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# SUBMIT PATIENT DATA
# -------------------------
@app.route("/add", methods=["POST"])
def add_patient():
    temp = request.form["temperature"]
    spo2 = request.form["spo2"]
    rr = request.form["rr"]

    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO vitals (temperature, spo2, rr)
        VALUES (?, ?, ?)
    """, (temp, spo2, rr))
    conn.commit()
    conn.close()

    return redirect("/view")

# -------------------------
# VIEW DATA
# -------------------------
@app.route("/view")
def view_data():
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute("SELECT * FROM vitals")
    rows = c.fetchall()
    conn.close()

    return render_template("view.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)