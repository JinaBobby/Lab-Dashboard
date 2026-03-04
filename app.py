from flask import Flask, redirect
from dashboards.lab.lab_routes import lab_bp
import os
import sqlite3
import random
import math
import pandas as pd

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

from tensorflow import keras
import numpy as np
from PIL import Image
app = Flask(__name__)
app.secret_key = "knowurbite_secret"

# Register lab blueprint
app.register_blueprint(lab_bp)

@app.route("/")
def home():
    return redirect("/lab_login/1")
import pandas as pd
@app.route("/lab_dashboard")
def lab_dashboard():
    lab_id = session.get("lab_id")
    
    # Safety check: if no lab_id in session, go back to login
    if not lab_id:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        SELECT enose_status, spectrometer_status 
        FROM labs 
        WHERE id=?
    """, (lab_id,))
    
    equipment_row = c.fetchone() 
    conn.close()

    if not equipment_row:
        equipment_row = ("Available", "Available")

    # Defined as an empty list to prevent a NameError crash. 
    # Add your real submissions database fetch here later!
    submissions = []

    return render_template(
        "lab_dashboard.html", 
        lab_id=lab_id, 
        equipment=equipment_row, 
        submissions=submissions
    )

@app.route("/update_equipment", methods=["POST"])
def update_equipment():
    lab_id = session.get("lab_id")

    enose = request.form.get("enose_status")
    spectrometer = request.form.get("spectrometer_status")

    if lab_id:
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # 1. Try to update the existing row
        c.execute("""
        UPDATE labs
        SET enose_status=?, spectrometer_status=?
        WHERE id=?
        """, (enose, spectrometer, lab_id))

        # 2. If 0 rows were updated, the lab_id doesn't exist yet! Let's insert it.
        if c.rowcount == 0:
            print(f"Lab {lab_id} not found! Inserting new row...")
            c.execute("""
                INSERT INTO labs (id, enose_status, spectrometer_status) 
                VALUES (?, ?, ?)
            """, (lab_id, enose, spectrometer))
        else:
            print(f"Successfully updated Lab {lab_id}!")

        conn.commit()
        conn.close()

    return redirect("/lab_dashboard")
@app.route('/lab_login/<int:lab_id>')
def lab_login(lab_id):
    session['lab_id'] = lab_id
    return redirect(url_for('lab_dashboard'))
@app.route("/find_lab", methods=["POST"])
def find_lab():

    device = request.form["device"]
    state = request.form["state"]

    labs = pd.read_excel("fssai_contact_with_devices.xlsx")

    result = labs[
        (labs["State"].str.lower()==state.lower()) &
        (labs[device]=="Yes")
    ]

    matched_labs = result.to_dict(orient="records")

    return render_template(
        "lab_dashboard.html",
        lab_id=session["lab_id"],
        equipment=("Available","Available"),
        matched_labs=matched_labs
    )

if __name__ == "__main__":
    app.run(debug=True)