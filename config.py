import os


class Config:
    """Application Configuration"""

    # Flask
    SECRET_KEY = os.environ.get(
        "FLASK_SECRET_KEY",
        "nexthire_super_secret_key"
    )

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///nexthire.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini API
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # Upload Folder
    UPLOAD_FOLDER = "uploads"

    # Maximum upload size (10 MB)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Allowed resume extensions
    ALLOWED_EXTENSIONS = {
        "pdf",
        "png",
        "jpg",
        "jpeg"
    }

    # Resume Settings
    MAX_NAME_LENGTH = 100
    MAX_ADDRESS_LENGTH = 250

    # ATS
    ATS_MAX_RESUME_CHARS = 15000
