from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

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
            patient_id TEXT,
            temperature REAL,
            spo2 INTEGER,
            rr INTEGER,
            timestamp TEXT
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
# ADD DATA
# -------------------------
@app.route("/add", methods=["POST"])
def add_patient():
    patient_id = request.form["patient_id"]
    temperature = request.form["temperature"]
    spo2 = request.form["spo2"]
    rr = request.form["rr"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("patients.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO vitals (patient_id, temperature, spo2, rr, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, temperature, spo2, rr, timestamp))

    conn.commit()
    conn.close()

    return redirect("/patients")

# -------------------------
# PATIENT LIST
# -------------------------
@app.route("/patients")
def patients():
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()

    c.execute("SELECT DISTINCT patient_id FROM vitals")
    rows = c.fetchall()

    conn.close()

    return render_template("patients.html", rows=rows)

# -------------------------
# PATIENT HISTORY
# -------------------------
@app.route("/patient/<patient_id>")
def patient_history(patient_id):
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()

    c.execute("""
        SELECT * FROM vitals
        WHERE patient_id = ?
        ORDER BY timestamp DESC
    """, (patient_id,))

    rows = c.fetchall()

    conn.close()

    return render_template("history.html", rows=rows, patient_id=patient_id)

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)