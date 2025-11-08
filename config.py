import os
from dotenv import load_dotenv

load_dotenv()

ALX_EMAIL = os.getenv("ALX_EMAIL")
ALX_PASSWORD = os.getenv("ALX_PASSWORD")

# Ensure credentials are set
if not ALX_EMAIL or not ALX_PASSWORD:
    raise ValueError("ALX_EMAIL and ALX_PASSWORD must be set in the .env file")
