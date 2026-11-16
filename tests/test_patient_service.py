
import pytest

from modules import patient_service


def test_patient_service_create_read_update_delete():
    patient_service.initialize_patient_service()

    # Create
    patient_id = patient_service.add_patient(
        "Service Test Patient",
        "15.05.1995",
        "service@example.com",
        95,
        14.2,
        180
    )

    assert patient_id is not None

    # Read
    patient = patient_service.get_patient(patient_id)
    assert patient["full_name"] == "Service Test Patient"

    # Update
    updated = patient_service.edit_patient(
        patient_id,
        "Service Updated Patient",
        "15.05.1995",
        "updated-service@example.com",
        100,
        14.5,
        185
    )

    assert updated is True

    patient = patient_service.get_patient(patient_id)
    assert patient["email"] == "updated-service@example.com"

    # Delete
    deleted = patient_service.remove_patient(patient_id)
    assert deleted is True


def test_duplicate_patient_rejected():
    patient_service.initialize_patient_service()

    patient_data = (
        "Duplicate Test Patient",
        "15.05.1995",
        "duplicate@example.com",
        95,
        14.2,
        180
    )

    patient_service.add_patient(*patient_data)

    with pytest.raises(ValueError, match="exact patient record"):
        patient_service.add_patient(*patient_data)

    # Clean up the test record.
    for patient in patient_service.list_patients():
        if patient["email"] == "duplicate@example.com":
            patient_service.remove_patient(patient["id"])
