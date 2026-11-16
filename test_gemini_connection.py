
from modules.ai_service import generate_health_remarks


print("Testing Gemini API connection...")

try:
    remarks = generate_health_remarks(
        dob="01/01/1990",
        glucose=95,
        haemoglobin=14,
        cholesterol=180
    )

    print("\nGemini API connection successful!")
    print("\nAI-generated health remarks:")
    print(remarks)

except Exception as error:
    print("\nGemini API connection failed.")
    print("Error:", error)
