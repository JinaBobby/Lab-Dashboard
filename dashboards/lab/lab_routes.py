from flask import Blueprint, render_template, session, redirect
import sqlite3

lab_bp = Blueprint("lab", __name__)

@lab_bp.route("/lab_login/<int:lab_id>")
def lab_login(lab_id):
    session["lab_id"] = lab_id
    return redirect("/lab_dashboard")


@lab_bp.route("/lab_dashboard")
def lab_dashboard():

    lab_id = session.get("lab_id")

    if not lab_id:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Get equipment info
    c.execute("""
    SELECT enose_status, spectrometer_status
    FROM labs
    WHERE id=?
    """, (lab_id,))

    equipment = c.fetchone()

    # Dummy values for dashboard
    submissions = []
    total_assigned = 0
    completed = 0
    pending = 0

    conn.close()

    return render_template(
        "lab_dashboard.html",
        lab_id=lab_id,
        equipment=equipment,
        submissions=submissions,
        total_assigned=total_assigned,
        completed=completed,
        pending=pending
    )