import sqlite3
import pandas as pd
from datetime import datetime


def create_database():
    conn = sqlite3.connect("attendance.db") # Creates attendance.db file
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   total_days INTEGER,
                   weekends INTEGER,
                   leaves INTEGER,
                   office_visits INTEGER,
                   attendance_percentage REAL,
                   timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to Insert Attendance Record
def insert_attendance(total_days, weekends, leaves, office_visits, attendance_percentage):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (total_days, weekends, leaves, office_visits, attendance_percentage, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?)
        """, (total_days, weekends, leaves, office_visits, attendance_percentage, datetime.now()))
    
    conn.commit()
    conn.close()

# Function to Fetch Attendance History

def fetch_history():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance ORDER BY timestamp DESC LIMIT 5") # Get last 5 records
    records = cursor.fetchall()
    conn.close()
    return records


# Export Attendance Data to Excel
def export_to_excel():
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()
    df.to_excel("Attendance_Report.xlsx", index=False)
    print("✅ Attendance report saved as 'Attendance_Report.xlsx'")

# Create Database Table (Run this once)

create_database()
