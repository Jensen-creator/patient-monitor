from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
from datetime import datetime

app = FastAPI()


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
@app.get("/", response_class=HTMLResponse)
def home(success: bool = False):

    success_html = ""
    if success:
        success_html = """
        <p id="success-msg" style="color: green; font-weight: bold;">
            Successfully submitted!
        </p>
        """

    return f"""
    <html>
    <head>
        <title>Patient Monitor</title>

        <style>
            body {{ font-family: Arial; margin: 40px; }}
            input {{ padding: 8px; margin: 5px; }}
            button {{ padding: 10px; background: green; color: white; border: none; }}
            table {{ margin-top: 20px; border-collapse: collapse; width: 100%; }}
            td, th {{ border: 1px solid #ccc; padding: 8px; }}
        </style>
    </head>

    <body>

        <h2>Patient Vitals Entry</h2>

        <form action="/vitals" method="post">
            Patient ID: <input name="patient_id" required><br>
            Temperature: <input name="temperature" type="number" step="0.1" required><br>
            SpO2: <input name="spo2" type="number" required><br>
            RR: <input name="rr" type="number" required><br>
            <button type="submit">Submit</button>
        </form>

        {success_html}

        <br>
        <a href="/view">View Records</a>

        <script>
            const successMsg = document.getElementById('success-msg');

            if (successMsg) {{
                document.querySelectorAll('input').forEach(input => {{
                    input.addEventListener('input', () => {{
                        successMsg.style.display = 'none';
                    }});
                }});
            }}
        </script>

    </body>
    </html>
    """


# -------------------------
# ADD DATA
# -------------------------
@app.post("/vitals")
def add_vitals(
    patient_id: str = Form(...),
    temperature: float = Form(...),
    spo2: int = Form(...),
    rr: int = Form(...)
):

    conn = sqlite3.connect("patients.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO vitals (patient_id, temperature, spo2, rr, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient_id,
        temperature,
        spo2,
        rr,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    # redirect back to homepage with success flag
    return RedirectResponse(url="/?success=true", status_code=303)


# -------------------------
# VIEW DATA PAGE
# -------------------------
@app.get("/view", response_class=HTMLResponse)
def view():

    conn = sqlite3.connect("patients.db")
    c = conn.cursor()

    c.execute("SELECT * FROM vitals ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    html_rows = ""

    for r in rows:
        html_rows += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td>{r[3]}</td>
            <td>{r[4]}</td>
            <td>{r[5]}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Patient Records</title>

        <style>
            body {{ font-family: Arial; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background: #f2f2f2; }}
        </style>
    </head>

    <body>

        <h2>All Patient Records</h2>

        <a href="/">← Back</a>

        <table>
            <tr>
                <th>ID</th>
                <th>Patient ID</th>
                <th>Temperature</th>
                <th>SpO2</th>
                <th>RR</th>
                <th>Timestamp</th>
            </tr>

            {html_rows}
        </table>

    </body>
    </html>
    """