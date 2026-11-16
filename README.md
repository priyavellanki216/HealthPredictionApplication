
# Health Prediction Application

A Python-based patient management application that stores blood test records and generates AI-assisted health observations using the Google Gemini API.

## Features

- Register patient records.
- View all saved patient records.
- Update existing patient information.
- Delete patient records.
- Validate patient names, email addresses, dates of birth and numeric blood-test values.
- Prevent duplicate patient records.
- Store patient information persistently using SQLite.
- Generate and save AI-assisted health remarks using Google Gemini.
- Display appropriate validation and API error messages.

## Technology Stack

- Python 3.12
- Streamlit
- SQLite
- Pandas
- Google Gemini API
- python-dotenv
- Pytest

## Project Structure

```text
HealthPredictionApp/
├── database/
│   ├── __init__.py
│   └── db.py
├── modules/
│   ├── __init__.py
│   ├── validation.py
│   ├── patient_service.py
│   └── ai_service.py
├── tests/
├── prompts/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.12 or later
- Google Gemini API key
- Internet connection for AI-generated remarks

## Installation

1. Clone or download the project.

2. Open the project directory in the terminal.

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the environment.

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

1. Create a `.env` file in the project root.
2. Add your Gemini API key:

   ```env
   GEMINI_API_KEY=your_actual_api_key
   GEMINI_MODEL=gemini-3.8-flash
   ```

3. Replace the placeholder with your own API key.

Never commit or share the `.env` file.

## Run the Application

From the project root, execute:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Run Automated Tests

Execute:

```bash
python -m pytest -v
```

The project's backend test suite passed all 13 automated tests during development.

## Data Validation

The application validates:

- Required patient names.
- Email address format.
- Date of birth format (DD/MM/YYYY or DD.MM.YYYY).
- Invalid calendar dates.
- Future dates of birth.
- Numeric, finite and non-negative blood-test values.
- Duplicate patient records.

## AI Integration

The application uses the Google Gemini API to generate informational observations from a patient's age and blood-test values.

Patient names and email addresses are not included in the AI prompt.

AI-generated remarks are stored with the corresponding patient record.

If the AI service is temporarily unavailable, the patient record remains saved and AI remarks can be generated again from the AI Remarks section.

## Important Health Disclaimer

AI-generated remarks are informational only and are not a medical diagnosis. Blood-test interpretation depends on measurement units, laboratory reference ranges, medical history and other clinical factors.

Users should consult qualified healthcare professionals for medical interpretation.

## Testing Summary

The application was tested using the ten patient records supplied in the assignment.

- Six unique valid patient records were accepted.
- Invalid email addresses were rejected.
- Invalid and future dates were rejected.
- Duplicate records were prevented.
- Patient creation, reading, updating and deletion were demonstrated.
- All 13 automated backend tests passed.

## Author

Developed as part of the Health Prediction Application assignment for Gokul Infocare.
