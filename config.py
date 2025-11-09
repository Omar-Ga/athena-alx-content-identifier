import os

from dotenv import load_dotenv

load_dotenv()

ALX_EMAIL = os.getenv("ALX_EMAIL")
ALX_PASSWORD = os.getenv("ALX_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure credentials are set
if not ALX_EMAIL or not ALX_PASSWORD or not GEMINI_API_KEY:
    raise ValueError(
        "ALX_EMAIL, ALX_PASSWORD, and GEMINI_API_KEY must be set in the .env file"
    )

MAX_PAGES = 1
