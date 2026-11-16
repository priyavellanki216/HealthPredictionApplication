
import pytest

from modules.ai_service import (
    calculate_age,
    generate_health_remarks
)


def test_calculate_age():
    age = calculate_age("01/01/2000")

    assert age >= 26


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="API key is missing"):
        generate_health_remarks(
            dob="01/01/2000",
            glucose=95,
            haemoglobin=14,
            cholesterol=180
        )
