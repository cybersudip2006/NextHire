import os


class Config:
    """NextHire application configuration."""

    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "nexthire_super_secret_key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///nexthire.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

    MAX_NAME_LENGTH = 100
    MAX_ADDRESS_LENGTH = 250

    ATS_MAX_RESUME_CHARS = 15000

    DEFAULT_TEMPLATE = "ats"

    PDF_MAX_PAGES = 5
    MAX_SKILLS = 30
    MAX_PROJECTS = 10
