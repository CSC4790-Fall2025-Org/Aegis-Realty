import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Aegis Realty"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    FIREBASE_CREDENTIALS: str = os.getenv("FIREBASE_CREDENTIALS", "")
    GOOGLE_GENAI_KEY: str = os.getenv("GOOGLE_GENAI_KEY", "")
    RENTCAST_API_KEY: str = os.getenv("RENTCAST_API_KEY", "")

settings = Settings()
