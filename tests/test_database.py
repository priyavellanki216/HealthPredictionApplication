
from database import db


def test_database_crud_operations():
    # Initialize the database.
    db.initialize_db()

    # Create a patient.
    patient_id = db.create_patient(
        full_name="Test Patient",
        dob="15/05/1995",
        email="test@example.com",
        glucose=95,
        haemoglobin=14.2,
        cholesterol=180
    )

    assert patient_id is not None

    # Read the patient.
    patient = db.get_patient_by_id(patient_id)

    assert patient is not None
    assert patient["full_name"] == "Test Patient"

    # Update the patient.
    updated = db.update_patient(
        patient_id=patient_id,
        full_name="Updated Patient",
        dob="15/05/1995",
        email="updated@example.com",
        glucose=100,
        haemoglobin=14.5,
        cholesterol=185,
        remarks="Test remarks"
    )

    assert updated is True

    patient = db.get_patient_by_id(patient_id)
    assert patient["email"] == "updated@example.com"

    # Delete the patient.
    deleted = db.delete_patient(patient_id)

    assert deleted is True
    assert db.get_patient_by_id(patient_id) is None
