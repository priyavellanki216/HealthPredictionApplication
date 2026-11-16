
import re
import math
from datetime import datetime, date


def validate_name(full_name):
    """Check that the patient's name is provided."""
    if not isinstance(full_name, str) or not full_name.strip():
        raise ValueError("Full name is required.")

    return full_name.strip()


def validate_email(email):
    """Validate a basic email address format."""
    if not isinstance(email, str):
        raise ValueError("Email address must be text.")

    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        raise ValueError("Please enter a valid email address.")

    return email


def validate_dob(dob):
    """
    Validate date of birth.
    Accept dd/mm/yyyy and dd.mm.yyyy formats.
    Return the date in dd/mm/yyyy format.
    """
    if not isinstance(dob, str):
        raise ValueError("Date of birth must be text.")

    dob = dob.strip()

    parsed_date = None

    for date_format in ("%d/%m/%Y", "%d.%m.%Y"):
        try:
            parsed_date = datetime.strptime(
                dob, date_format
            ).date()
            break
        except ValueError:
            continue

    if parsed_date is None:
        raise ValueError(
            "Invalid date. Use dd/mm/yyyy or dd.mm.yyyy."
        )

    if parsed_date > date.today():
        raise ValueError("Date of birth cannot be in the future.")

    return parsed_date.strftime("%d/%m/%Y")


def validate_numeric_value(value, field_name):
    """Ensure a blood test value is numeric and non-negative."""
    try:
        if isinstance(value, bool):
            raise ValueError

        numeric_value = float(value)

    except (TypeError, ValueError):
        raise ValueError(
            f"{field_name} must be a numeric value."
        )

    if not math.isfinite(numeric_value):
        raise ValueError(
            f"{field_name} must be a finite numeric value."
        )

    if numeric_value < 0:
        raise ValueError(
            f"{field_name} cannot be negative."
        )

    return numeric_value


def validate_patient_data(
    full_name,
    dob,
    email,
    glucose,
    haemoglobin,
    cholesterol
):
    """Validate all patient fields and return cleaned data."""

    return {
        "full_name": validate_name(full_name),
        "dob": validate_dob(dob),
        "email": validate_email(email),
        "glucose": validate_numeric_value(
            glucose, "Glucose"
        ),
        "haemoglobin": validate_numeric_value(
            haemoglobin, "Haemoglobin"
        ),
        "cholesterol": validate_numeric_value(
            cholesterol, "Cholesterol"
        )
    }
