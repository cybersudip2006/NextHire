import os
import re
import textwrap
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename, allowed_extensions=None):
    allowed_extensions = allowed_extensions or ALLOWED_EXTENSIONS
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_REGEX = re.compile(r"^\+?[0-9 ]{8,20}$")
URL_REGEX = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)


def is_valid_email(email):
    return bool(email and EMAIL_REGEX.match(email))


def is_valid_phone(phone):
    return bool(phone and PHONE_REGEX.match(phone))


def is_valid_url(url):
    if not url:
        return True
    return bool(URL_REGEX.match(url))


def clean_text(text):
    if not text:
        return ""
    text = text.replace("\r", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def wrap_text(text, width=85):
    if not text:
        return []
    return textwrap.wrap(text, width)


def safe(value):
    if value is None:
        return ""
    return str(value).strip()


def year_range(start, end):
    start = safe(start)
    end = safe(end)

    if start and end:
        return f"{start} - {end}"

    if start:
        return f"{start} - Present"

    return ""


def ats_percentage(score):
    score = max(0, min(float(score or 0), 10))
    return int(score * 10)


def human_size(size):
    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.2f} MB"


def slugify(value):
    value = safe(value)
    value = re.sub(r"[^A-Za-z0-9 ]", "", value)
    return "_".join(value.split()) or "Resume"


def resume_filename(name):
    return f"{slugify(name)}_Resume.pdf"


def split_skills(skill_text):
    if not skill_text:
        return []
    return [item.strip() for item in skill_text.split(",") if item.strip()]


def save_uploaded_photo(files, upload_folder):
    if "profile_photo" not in files:
        return None

    photo = files["profile_photo"]

    if not photo or photo.filename == "":
        return None

    if not allowed_file(photo.filename, IMAGE_EXTENSIONS):
        return None

    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(photo.filename)
    path = os.path.join(upload_folder, filename)
    photo.save(path)

    return path


def has_photo(files):
    return "profile_photo" in files and files["profile_photo"].filename != ""


def format_title(title):
    return safe(title).upper()
