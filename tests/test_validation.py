
import pytest
from modules.validation import (
    validate_patient_data,
    validate_dob,
    validate_email
)


def test_valid_patient_data():
    patient = validate_patient_data(
        "Tenille Singh",
        "30.11.1991",
        "Tenille@yahoo.com",
        101,
        15,
        310
    )

    assert patient["full_name"] == "Tenille Singh"
    assert patient["dob"] == "30/11/1991"
    assert patient["glucose"] == 101.0


def test_invalid_email():
    with pytest.raises(ValueError):
        validate_email("hunter@gmail")


def test_invalid_email_without_at_symbol():
    with pytest.raises(ValueError):
        validate_email("Kris.wu.gmail.com")


def test_invalid_calendar_date():
    with pytest.raises(ValueError):
        validate_dob("31.11.2001")


def test_future_date():
    with pytest.raises(ValueError):
        validate_dob("19.10.2030")


def test_valid_date_with_slashes():
    assert validate_dob("30/11/1991") == "30/11/1991"


def test_negative_glucose():
    with pytest.raises(ValueError):
        validate_patient_data(
            "Test Patient",
            "15/05/1995",
            "test@example.com",
            -10,
            14,
            180
        )


def test_non_numeric_haemoglobin():
    with pytest.raises(ValueError):
        validate_patient_data(
            "Test Patient",
            "15/05/1995",
            "test@example.com",
            95,
            "abc",
            180
        )
