from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_change_this"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def init_db():
    conn = sqlite3.connect("crime_reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            location TEXT NOT NULL,
            crime_type TEXT NOT NULL,
            description TEXT NOT NULL,
            evidence TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        anonymous = request.form.get("anonymous")

        name = "Anonymous" if anonymous else request.form.get("name")
        phone = "Hidden" if anonymous else request.form.get("phone")

        location = request.form.get("location")
        crime_type = request.form.get("crime_type")
        description = request.form.get("description")

        file = request.files.get("evidence")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = sqlite3.connect("crime_reports.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reports 
            (name, phone, location, crime_type, description, evidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            location,
            crime_type,
            description,
            filename,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("success"))

    return render_template("report.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            error = "Invalid username or password"

    return render_template("admin_login.html", error=error)


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect("crime_reports.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    reports = cursor.fetchall()

    conn.close()

    return render_template("admin.html", reports=reports)


@app.route("/update-status/<int:report_id>", methods=["POST"])
def update_status(report_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    status = request.form.get("status")

    conn = sqlite3.connect("crime_reports.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE reports SET status = ? WHERE id = ?", (status, report_id))

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))