
import sqlite3
from pathlib import Path
from datetime import datetime


# Store the database inside the project's database folder.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "patients.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    """Create the patients table if it does not already exist."""
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT NOT NULL,
                glucose REAL NOT NULL,
                haemoglobin REAL NOT NULL,
                cholesterol REAL NOT NULL,
                remarks TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        connection.commit()
    finally:
        connection.close()


def create_patient(full_name, dob, email, glucose, haemoglobin, cholesterol):
    """Insert a new patient record and return its database ID."""
    connection = get_connection()
    timestamp = datetime.now().isoformat(timespec="seconds")

    try:
        cursor = connection.execute("""
            INSERT INTO patients (
                full_name, dob, email, glucose,
                haemoglobin, cholesterol, remarks,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, '', ?, ?)
        """, (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            timestamp,
            timestamp
        ))

        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_all_patients():
    """Return all patient records, newest first."""
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT * FROM patients
            ORDER BY id DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_patient_by_id(patient_id):
    """Return one patient record using its ID."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM patients WHERE id = ?",
            (patient_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def update_patient(patient_id, full_name, dob, email,
                   glucose, haemoglobin, cholesterol, remarks=None):
    """Update an existing patient record."""
    connection = get_connection()
    timestamp = datetime.now().isoformat(timespec="seconds")

    try:
        connection.execute("""
            UPDATE patients
            SET full_name = ?,
                dob = ?,
                email = ?,
                glucose = ?,
                haemoglobin = ?,
                cholesterol = ?,
                remarks = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks or '',
            timestamp,
            patient_id
        ))

        connection.commit()
        return connection.total_changes > 0
    finally:
        connection.close()


def update_patient_remarks(patient_id, remarks):
    """Save the AI-generated remarks for a patient."""
    connection = get_connection()

    try:
        cursor = connection.execute("""
            UPDATE patients
            SET remarks = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            remarks,
            datetime.now().isoformat(timespec="seconds"),
            patient_id
        ))

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_patient(patient_id):
    """Delete a patient record using its ID."""
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM patients WHERE id = ?",
            (patient_id,)
        )

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()
