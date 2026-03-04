import sqlite3

def find_best_lab(required_equipment, vendor_city, vendor_state):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT labs.id, labs.lab_name, labs.state
    FROM labs
    JOIN lab_equipment
    ON labs.id = lab_equipment.lab_id
    WHERE lab_equipment.equipment = ?
    """, (required_equipment,))

    labs = c.fetchall()

    # Priority 1: Same city
    for lab in labs:
        if lab[2] == vendor_city:
            conn.close()
            return lab

    # Priority 2: Same state
    for lab in labs:
        if lab[2] == vendor_state:
            conn.close()
            return lab

    conn.close()

    return labs[0] if labs else None