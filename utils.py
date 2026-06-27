import os
import re
import textwrap

# ==========================================
# ALLOWED FILES
# ==========================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):
    """
    Check uploaded file extension.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ==========================================
# EMAIL VALIDATION
# ==========================================

EMAIL_REGEX = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)


def is_valid_email(email):
    if not email:
        return False
    return EMAIL_REGEX.match(email) is not None


# ==========================================
# PHONE VALIDATION
# ==========================================

PHONE_REGEX = re.compile(r'^\+?[0-9 ]{8,20}$')


def is_valid_phone(phone):
    if not phone:
        return False
    return PHONE_REGEX.match(phone) is not None


# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    if not text:
        return ""

    text = text.replace("\r", "")

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ==========================================
# WORD WRAP
# ==========================================

def wrap_text(text, width=85):

    if not text:
        return []

    return textwrap.wrap(text, width)


# ==========================================
# ATS SCORE BAR
# ==========================================

def ats_percentage(score):

    if score < 0:
        score = 0

    if score > 10:
        score = 10

    return int(score * 10)


# ==========================================
# SAFE STRING
# ==========================================

def safe(value):

    if value is None:
        return ""

    return str(value).strip()


# ==========================================
# YEAR FORMAT
# ==========================================

def year_range(start, end):

    start = safe(start)

    end = safe(end)

    if start and end:
        return f"{start} - {end}"

    if start:
        return f"{start} - Present"

    return ""


# ==========================================
# FILE SIZE
# ==========================================

def human_size(size):

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size/1024:.1f} KB"

    return f"{size/(1024*1024):.2f} MB"


# ==========================================
# RESUME FILE NAME
# ==========================================

def resume_filename(name):

    name = safe(name)

    name = re.sub(r'[^A-Za-z0-9 ]', '', name)

    name = "_".join(name.split())

    if not name:
        name = "Resume"

    return f"{name}_Resume.pdf"


# ==========================================
# SKILLS
# ==========================================

def split_skills(skill_text):

    if not skill_text:
        return []

    skills = []

    for item in skill_text.split(","):

        item = item.strip()

        if item:

            skills.append(item)

    return skills


# ==========================================
# EXPERIENCE
# ==========================================

def has_experience(form):

    return bool(

        safe(form.get("exp_company"))

        or safe(form.get("experience"))

    )


# ==========================================
# EDUCATION
# ==========================================

def has_education(form):

    return bool(

        safe(form.get("edu_school"))

    )


# ==========================================
# PROJECTS
# ==========================================

def has_projects(form):

    return bool(

        safe(form.get("project_name"))

    )


# ==========================================
# CERTIFICATES
# ==========================================

def has_certificates(form):

    return bool(

        safe(form.get("certificate_name"))

    )


# ==========================================
# PHOTO
# ==========================================

def has_photo(files):

    if "profile_photo" not in files:
        return False

    photo = files["profile_photo"]

    return photo.filename != ""


# ==========================================
# SECTION TITLE
# ==========================================

def format_title(title):

    return title.upper()
