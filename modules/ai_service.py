
import os
from datetime import date, datetime

from dotenv import load_dotenv
from google import genai


# Load environment variables from the project's .env file.
load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def calculate_age(dob):
    """Calculate age from a date in dd/mm/yyyy format."""

    birth_date = datetime.strptime(dob, "%d/%m/%Y").date()
    today = date.today()

    age = today.year - birth_date.year

    if (today.month, today.day) < (
        birth_date.month, birth_date.day
    ):
        age -= 1

    return age


def generate_health_remarks(
    dob,
    glucose,
    haemoglobin,
    cholesterol
):
    """
    Generate informational health observations using Gemini.

    The output is not a medical diagnosis.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key is missing. "
            "Please configure GEMINI_API_KEY in your .env file."
        )

    age = calculate_age(dob)

    
    prompt = f"""
You are an AI assistant generating cautious,
informational health screening observations.

Review these patient values:

Age: {age} years
Glucose: {glucose}
Haemoglobin: {haemoglobin}
Cholesterol: {cholesterol}

Instructions:
1. Briefly assess glucose, haemoglobin, and cholesterol
   separately, identifying any possible health-risk signals.
2. Summarize any potential health concerns suggested by
   the combination of these values.
3. Do not diagnose any disease or claim certainty.
4. Do not prescribe medicines or treatment.
5. Do not invent measurement units or laboratory
   reference ranges.
6. Explain that interpretation depends on units, laboratory
   reference ranges, medical history, and fasting status.
7. Recommend discussing concerning results with a qualified
   healthcare professional.
8. Use simple, clear language.
9. Keep the response between 80 and 130 words.
10. State that the output is AI-generated information,
    not a medical diagnosis.

Return only the health observations.
"""


    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        remarks = response.text

        if not remarks or not remarks.strip():
            raise RuntimeError(
                "The AI API returned an empty response."
            )

        return remarks.strip()

    except Exception as error:
        raise RuntimeError(
            f"Gemini API request failed: {error}"
        ) from error
