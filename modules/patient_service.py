
from database import db
from modules.validation import validate_patient_data


def initialize_patient_service():
    """Initialize the patient database."""
    db.initialize_db()


def add_patient(
    full_name,
    dob,
    email,
    glucose,
    haemoglobin,
    cholesterol
):
    """Validate and save a new patient."""

    patient = validate_patient_data(
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol
    )

    # Check for an exact duplicate before insertion.
    existing_patients = db.get_all_patients()

    for existing in existing_patients:
        if (
            existing["full_name"].casefold()
            == patient["full_name"].casefold()
            and existing["dob"] == patient["dob"]
            and existing["email"].casefold()
            == patient["email"].casefold()
            and float(existing["glucose"]) == patient["glucose"]
            and float(existing["haemoglobin"]) == patient["haemoglobin"]
            and float(existing["cholesterol"]) == patient["cholesterol"]
        ):
            raise ValueError(
                "This exact patient record already exists."
            )

    patient_id = db.create_patient(
        full_name=patient["full_name"],
        dob=patient["dob"],
        email=patient["email"],
        glucose=patient["glucose"],
        haemoglobin=patient["haemoglobin"],
        cholesterol=patient["cholesterol"]
    )

    return patient_id


def list_patients():
    """Return all saved patients."""
    return db.get_all_patients()


def get_patient(patient_id):
    """Get one patient by ID."""
    patient = db.get_patient_by_id(patient_id)

    if patient is None:
        raise ValueError("Patient record not found.")

    return patient


def edit_patient(
    patient_id,
    full_name,
    dob,
    email,
    glucose,
    haemoglobin,
    cholesterol
):
    """Validate and update a patient."""

    patient = validate_patient_data(
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol
    )

    existing = db.get_patient_by_id(patient_id)

    if existing is None:
        raise ValueError("Patient record not found.")

    return db.update_patient(
        patient_id=patient_id,
        full_name=patient["full_name"],
        dob=patient["dob"],
        email=patient["email"],
        glucose=patient["glucose"],
        haemoglobin=patient["haemoglobin"],
        cholesterol=patient["cholesterol"],
        remarks=existing["remarks"]
    )


def remove_patient(patient_id):
    """Delete a patient."""
    if db.get_patient_by_id(patient_id) is None:
        raise ValueError("Patient record not found.")

    return db.delete_patient(patient_id)
