import pandas as pd
import sqlite3

# Load Excel file
df = pd.read_excel("FSSAI contact.xlsx")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS labs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_no INTEGER,
    lab_name TEXT,
    registration_number TEXT,
    nabl_certificate_number TEXT,
    nabl_fssai_integrated TEXT,
    state TEXT,
    contact_person TEXT,
    phone TEXT,
    email TEXT
)
""")

cursor.execute("DELETE FROM labs")

for _, row in df.iterrows():

    cursor.execute("""
    INSERT INTO labs (
        serial_no,
        lab_name,
        registration_number,
        nabl_certificate_number,
        nabl_fssai_integrated,
        state,
        contact_person,
        phone,
        email
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        int(row["S.No"]),
        row["Lab Name"],
        row["Registration Number"],
        row["NABL Certificate Number"],
        row["NABL-FSSAI Integrated (Y/N)"],
        row["State"],
        row["Contact Person"],
        str(row["Phone"]),
        row["Email"]
    ))

conn.commit()

cursor.execute("SELECT COUNT(*) FROM labs")
print("Total labs inserted:", cursor.fetchone()[0])

conn.close()