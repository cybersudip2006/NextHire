import io
import os

from flask import send_file

try:
    from PIL import Image as PILImage, ImageDraw, ImageOps
except Exception:
    PILImage = None
    ImageDraw = None
    ImageOps = None

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

styles = getSampleStyleSheet()


# =====================================================
# COMMON COLORS
# =====================================================

COLORS = {

    "blue": colors.HexColor("#2563EB"),
    "black": colors.HexColor("#111827"),
    "green": colors.HexColor("#059669"),
    "purple": colors.HexColor("#7C3AED"),
    "orange": colors.HexColor("#EA580C"),
    "gray": colors.HexColor("#64748B"),
    "light": colors.HexColor("#F8FAFC")

}


# =====================================================
# CREATE DOCUMENT
# =====================================================

def create_document():

    buffer = io.BytesIO()

    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=35,
        leftMargin=35,

        topMargin=35,
        bottomMargin=35

    )

    return document, buffer
# =====================================================
# SHOULD INCLUDE SECTION
# =====================================================

def include_section(form, field_name):

    value = form.get(field_name)

    if value is None:
        return False

    value = str(value).strip().lower()

    return value in ("true", "1", "yes", "on")

# =====================================================
# TITLE
# =====================================================

def add_title(story, title):

    style = styles["Heading1"]

    style.textColor = COLORS["blue"]

    story.append(

        Paragraph(title, style)

    )

    story.append(

        Spacer(1,12)

    )


# =====================================================
# SUB TITLE
# =====================================================

def add_heading(story, text):

    style = styles["Heading2"]

    style.textColor = COLORS["blue"]

    story.append(

        Paragraph(text, style)

    )

    story.append(

        Spacer(1,6)

    )


# =====================================================
# NORMAL TEXT
# =====================================================

def add_text(story,text):

    story.append(

        Paragraph(text,styles["BodyText"])

    )

    story.append(

        Spacer(1,6)

    )


# =====================================================
# HORIZONTAL LINE
# =====================================================

def add_line(story):

    table=Table(

        [[""]],

        colWidths=[500]

    )

    table.setStyle(

        TableStyle([

            ("LINEBELOW",(0,0),(-1,-1),1,COLORS["gray"])

        ])

    )

    story.append(table)

    story.append(

        Spacer(1,10)

    )


# =====================================================
# PROFILE IMAGE
# =====================================================

def add_profile_photo(story,image_path):

    if image_path and os.path.exists(image_path):

        img=Image(

            image_path,

            width=1.2*inch,

            height=1.2*inch

        )

        story.append(img)

        story.append(

            Spacer(1,12)

        )



# =====================================================
# CIRCULAR PROFILE PHOTO SUPPORT
# =====================================================

def photo_enabled(form):

    value = form.get("include_photo")

    if value is None:
        return True

    return str(value).strip().lower() in ("true", "1", "yes", "on")


def create_circular_photo(form, files, size=1.2*inch):

    if not files:
        return None

    if not photo_enabled(form):
        return None

    uploaded = files.get("profile_photo")

    if not uploaded or uploaded.filename == "":
        return None

    if PILImage is None:
        return None

    try:
        uploaded.stream.seek(0)

        image = PILImage.open(uploaded.stream)

        image = ImageOps.exif_transpose(image)

        image = image.convert("RGBA")

        image = ImageOps.fit(
            image,
            (700, 700),
            method=PILImage.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )

        mask = PILImage.new("L", (700, 700), 0)

        draw = ImageDraw.Draw(mask)

        draw.ellipse((0, 0, 700, 700), fill=255)

        image.putalpha(mask)

        buffer = io.BytesIO()

        image.save(buffer, format="PNG", optimize=True)

        buffer.seek(0)

        return Image(
            buffer,
            width=size,
            height=size
        )

    except Exception:
        return None


def add_template_photo(story, form, files=None, template="default"):

    if template == "ats":
        return

    if not files:
        return

    if template == "creative":
        size = 1.65 * inch

    elif template == "executive":
        size = 1.35 * inch

    else:
        size = 1.15 * inch

    photo = create_circular_photo(form, files, size)

    if not photo:
        return

    if template == "creative":

        table = Table(
            [[photo]],
            colWidths=[500]
        )

        table.setStyle(TableStyle([
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 14)
        ]))

        story.append(table)

        return

    if template == "executive":

        table = Table(
            [[photo, ""]],
            colWidths=[size + 10, 500 - size]
        )

        table.setStyle(TableStyle([
            ("ALIGN", (0,0), (0,0), "LEFT"),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10)
        ]))

        story.append(table)

        return

    table = Table(
        [["", photo]],
        colWidths=[500 - size, size]
    )

    table.setStyle(TableStyle([
        ("ALIGN", (1,0), (1,0), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10)
    ]))

    story.append(table)


# =====================================================
# DYNAMIC SECTION
# =====================================================

def section(story,title,value):

    if not value:

        return

    if str(value).strip()=="":

        return

    add_heading(story,title)

    add_text(story,value)


# =====================================================
# EDUCATION
# =====================================================

def education_section(story, form):

    if not include_section(form, "include_education"):
        return

    school = form.get("edu_school", "")

    if school.strip() == "":
        return

    start = form.get("edu_start", "")
    end = form.get("edu_end", "")
    degree = form.get("degree", "")
    grade = form.get("cgpa", "")

    add_heading(story, "Education")

    txt = f"<b>{school}</b><br/>"

    if degree:
        txt += degree + "<br/>"

    if start or end:
        txt += f"{start} - {end}<br/>"

    if grade:
        txt += f"CGPA : {grade}"

    add_text(story, txt)

# =====================================================
# EXPERIENCE
# =====================================================

def experience_section(story, form):

    if not include_section(form, "include_experience"):
        return

    company = form.get("exp_company", "")

    if company.strip() == "":
        return

    start = form.get("exp_start", "")
    end = form.get("exp_end", "")
    role = form.get("exp_role", "")
    desc = form.get("exp_desc", "")

    add_heading(story, "Experience")

    txt = f"<b>{company}</b><br/>"

    if role:
        txt += role + "<br/>"

    if start or end:
        txt += f"{start} - {end}<br/>"

    txt += desc

    add_text(story, txt)

# =====================================================
# PROJECTS
# =====================================================

def projects_section(story, form):

    if not include_section(form, "include_projects"):
        return

    project = form.get("project", "")

    if project.strip() == "":
        return

    add_heading(story, "Projects")

    add_text(story, project)
# =====================================================
# SKILLS
# =====================================================

def skills_section(story, form):

    if not include_section(form, "include_skills"):
        return

    skills = form.get("skills", "")

    if skills.strip() == "":
        return

    add_heading(story, "Skills")

    add_text(story, skills)


# =====================================================
# CERTIFICATIONS
# =====================================================

def certification_section(story, form):

    if not include_section(form, "include_certifications"):
        return

    cert = form.get("certification", "")

    if cert.strip() == "":
        return

    add_heading(story, "Certifications")

    add_text(story, cert)
# =====================================================
# ACHIEVEMENTS
# =====================================================

def achievement_section(story, form):

    if not include_section(form, "include_achievements"):
        return

    ach = form.get("achievement", "")

    if ach.strip() == "":
        return

    add_heading(story, "Achievements")

    add_text(story, ach)

# =====================================================
# LANGUAGES
# =====================================================

def language_section(story, form):

    if not include_section(form, "include_languages"):
        return

    lang = form.get("languages", "")

    if lang.strip() == "":
        return

    add_heading(story, "Languages")

    add_text(story, lang)
  # =====================================================
# ATS OPTIMIZED TEMPLATE
# =====================================================

def ats_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_title(
        story,
        form.get("name", "")
    )

    contact = f"""
<b>Email:</b> {form.get('email','')}<br/>
<b>Phone:</b> {form.get('country_code','')} {form.get('phone','')}<br/>
<b>Address:</b> {form.get('address','')}
"""

    add_text(story, contact)

    add_line(story)

    section(
        story,
        "Professional Summary",
        form.get("objective","")
    )

    education_section(story, form)

    experience_section(story, form)

    projects_section(story, form)

    skills_section(story, form)

    certification_section(story, form)

    achievement_section(story, form)

    language_section(story, form)

    document.build(story)

    buffer.seek(0)

    return buffer


# =====================================================
# MODERN BLUE TEMPLATE
# =====================================================

def modern_blue_template(form, files=None):

    document, buffer = create_document()

    story=[]

    add_template_photo(story, form, files, "modern_blue")

    style=styles["Heading1"]

    style.textColor=COLORS["blue"]

    style.fontSize=24

    story.append(
        Paragraph(
            form.get("name",""),
            style
        )
    )

    story.append(
        Spacer(1,8)
    )

    contact=f"""

<b>Email</b> : {form.get("email","")} &nbsp;&nbsp;&nbsp;

<b>Phone</b> : {form.get("country_code","")} {form.get("phone","")}<br/>

<b>Address</b> : {form.get("address","")}

"""

    add_text(story,contact)

    add_line(story)

    section(
        story,
        "Career Objective",
        form.get("objective","")
    )

    education_section(story,form)

    experience_section(story,form)

    projects_section(story,form)

    skills_section(story,form)

    certification_section(story,form)

    achievement_section(story,form)

    language_section(story,form)

    document.build(story)

    buffer.seek(0)

    return buffer


# =====================================================
# PROFESSIONAL BLACK TEMPLATE
# =====================================================

def professional_black_template(form, files=None):

    document,buffer=create_document()

    story=[]

    add_template_photo(story, form, files, "professional_black")

    style=styles["Heading1"]

    style.textColor=COLORS["black"]

    style.fontSize=25

    story.append(

        Paragraph(

            form.get("name",""),

            style

        )

    )

    story.append(

        Spacer(1,10)

    )

    contact=f"""

{form.get("email","")} |
{form.get("country_code","")} {form.get("phone","")} |
{form.get("address","")}

"""

    add_text(story,contact)

    add_line(story)

    section(

        story,

        "Professional Summary",

        form.get("objective","")

    )

    education_section(story,form)

    experience_section(story,form)

    projects_section(story,form)

    skills_section(story,form)

    certification_section(story,form)

    achievement_section(story,form)

    language_section(story,form)

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# MINIMAL CLEAN TEMPLATE
# =====================================================

def minimal_clean_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "minimal")

    # -----------------------------
    # Name
    # -----------------------------

    style = styles["Title"]

    style.textColor = COLORS["green"]

    style.fontSize = 24

    style.spaceAfter = 4

    story.append(
        Paragraph(
            form.get("name", ""),
            style
        )
    )

    # -----------------------------
    # Contact
    # -----------------------------

    contact = f"""
<font size=10>
{form.get('email','')} |
{form.get('country_code','')} {form.get('phone','')} |
{form.get('address','')}
</font>
"""

    story.append(
        Paragraph(contact, styles["BodyText"])
    )

    story.append(
        Spacer(1, 10)
    )

    add_line(story)

    # -----------------------------
    # Objective
    # -----------------------------

    section(
        story,
        "Professional Summary",
        form.get("objective", "")
    )

    # -----------------------------
    # Education
    # -----------------------------

    education_section(
        story,
        form
    )

    # -----------------------------
    # Experience
    # -----------------------------

    experience_section(
        story,
        form
    )

    # -----------------------------
    # Projects
    # -----------------------------

    projects_section(
        story,
        form
    )

    # -----------------------------
    # Skills
    # -----------------------------

    skills_section(
        story,
        form
    )

    # -----------------------------
    # Certifications
    # -----------------------------

    certification_section(
        story,
        form
    )

    # -----------------------------
    # Achievements
    # -----------------------------

    achievement_section(
        story,
        form
    )

    # -----------------------------
    # Languages
    # -----------------------------

    language_section(
        story,
        form
    )

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# EXECUTIVE TEMPLATE
# =====================================================

def executive_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "executive")

    # -----------------------------------------
    # Name
    # -----------------------------------------

    title = styles["Title"]

    title.textColor = COLORS["purple"]

    title.fontSize = 28

    title.spaceAfter = 6

    story.append(
        Paragraph(
            form.get("name", ""),
            title
        )
    )

    # -----------------------------------------
    # Contact
    # -----------------------------------------

    contact = f"""
<b>Email</b> : {form.get('email','')}<br/>
<b>Phone</b> : {form.get('country_code','')} {form.get('phone','')}<br/>
<b>Address</b> : {form.get('address','')}
"""

    story.append(
        Paragraph(contact, styles["BodyText"])
    )

    story.append(
        Spacer(1, 12)
    )

    # Purple Divider

    divider = Table(
        [[""]],
        colWidths=[520]
    )

    divider.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),COLORS["purple"]),

        ("BOTTOMPADDING",(0,0),(-1,-1),3)

    ]))

    story.append(divider)

    story.append(Spacer(1,15))

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    section(
        story,
        "Executive Summary",
        form.get("objective","")
    )

    # -----------------------------------------

    education_section(story, form)

    experience_section(story, form)

    projects_section(story, form)

    skills_section(story, form)

    certification_section(story, form)

    achievement_section(story, form)

    language_section(story, form)

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# CREATIVE TEMPLATE
# =====================================================

def creative_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "creative")

    # --------------------------------------------
    # Name
    # --------------------------------------------

    title = styles["Title"]

    title.textColor = COLORS["orange"]

    title.fontSize = 30

    title.spaceAfter = 8

    story.append(
        Paragraph(
            form.get("name", ""),
            title
        )
    )

    # --------------------------------------------
    # Contact Card
    # --------------------------------------------

    contact_data = [[

        Paragraph(f"<b>Email</b><br/>{form.get('email','')}", styles["BodyText"]),

        Paragraph(f"<b>Phone</b><br/>{form.get('country_code','')} {form.get('phone','')}", styles["BodyText"]),

        Paragraph(f"<b>Address</b><br/>{form.get('address','')}", styles["BodyText"])

    ]]

    contact_table = Table(
        contact_data,
        colWidths=[170,170,170]
    )

    contact_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),COLORS["light"]),

        ("GRID",(0,0),(-1,-1),0.4,colors.lightgrey),

        ("BOX",(0,0),(-1,-1),1,COLORS["orange"]),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("TOPPADDING",(0,0),(-1,-1),10),

        ("LEFTPADDING",(0,0),(-1,-1),12),

        ("RIGHTPADDING",(0,0),(-1,-1),12)

    ]))

    story.append(contact_table)

    story.append(Spacer(1,18))

    # --------------------------------------------
    # Summary
    # --------------------------------------------

    section(
        story,
        "Career Profile",
        form.get("objective","")
    )

    # --------------------------------------------

    education_section(story, form)

    experience_section(story, form)

    projects_section(story, form)

    skills_section(story, form)

    certification_section(story, form)

    achievement_section(story, form)

    language_section(story, form)

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# FRESHER RESUME TEMPLATE
# =====================================================

def fresher_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "fresher")

    title = styles["Title"]

    title.textColor = COLORS["blue"]

    title.fontSize = 26

    story.append(
        Paragraph(
            form.get("name",""),
            title
        )
    )

    story.append(Spacer(1,8))

    contact = f"""
<b>Email:</b> {form.get("email","")}<br/>
<b>Phone:</b> {form.get("country_code","")} {form.get("phone","")}<br/>
<b>Address:</b> {form.get("address","")}
"""

    add_text(story, contact)

    add_line(story)

    # Freshers start with objective

    section(
        story,
        "Career Objective",
        form.get("objective","")
    )

    # Education comes FIRST

    education_section(story, form)

    # Skills before Experience

    skills_section(story, form)

    # Projects

    projects_section(story, form)

    # Internship / Experience

    experience_section(story, form)

    # Certifications

    certification_section(story, form)

    # Achievements

    achievement_section(story, form)

    # Languages

    language_section(story, form)

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# STUDENT RESUME TEMPLATE
# =====================================================

def student_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "student")

    title = styles["Title"]

    title.textColor = COLORS["green"]

    title.fontSize = 26

    story.append(
        Paragraph(
            form.get("name", ""),
            title
        )
    )

    story.append(Spacer(1, 8))

    contact = f"""
<b>Email:</b> {form.get("email","")}<br/>
<b>Phone:</b> {form.get("country_code","")} {form.get("phone","")}<br/>
<b>Address:</b> {form.get("address","")}
"""

    add_text(story, contact)

    add_line(story)

    # Academic Objective

    section(
        story,
        "Career Objective",
        form.get("objective","")
    )

    # Education First

    education_section(story, form)

    # Academic Projects

    projects_section(story, form)

    # Technical Skills

    skills_section(story, form)

    # Internship

    experience_section(story, form)

    # Certifications

    certification_section(story, form)

    # Achievements

    achievement_section(story, form)

    # Extra Curricular Activities

    section(
        story,
        "Extra Curricular Activities",
        form.get("extra_curricular","")
    )

    # Positions of Responsibility

    section(
        story,
        "Positions of Responsibility",
        form.get("leadership","")
    )

    # Workshops

    section(
        story,
        "Workshops & Training",
        form.get("workshop","")
    )

    # Hackathons

    section(
        story,
        "Hackathons",
        form.get("hackathon","")
    )

    # Languages

    language_section(story, form)

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# EXPERIENCED PROFESSIONAL TEMPLATE
# =====================================================

def experienced_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "experienced")

    title = styles["Title"]
    title.textColor = COLORS["black"]
    title.fontSize = 26

    story.append(
        Paragraph(
            form.get("name", ""),
            title
        )
    )

    story.append(Spacer(1, 8))

    contact = f"""
<b>Email:</b> {form.get("email","")}<br/>
<b>Phone:</b> {form.get("country_code","")} {form.get("phone","")}<br/>
<b>Address:</b> {form.get("address","")}
"""

    add_text(story, contact)

    add_line(story)

    # Professional Summary

    section(
        story,
        "Professional Summary",
        form.get("objective","")
    )

    # Experience FIRST

    experience_section(story, form)

    # Skills

    skills_section(story, form)

    # Projects

    projects_section(story, form)

    # Certifications

    certification_section(story, form)

    # Achievements

    achievement_section(story, form)

    # Education

    education_section(story, form)

    # Languages

    language_section(story, form)

    # References

    section(
        story,
        "References",
        form.get(
            "references",
            "Available upon request."
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# SOFTWARE DEVELOPER TEMPLATE
# =====================================================

def software_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "software")

    title = styles["Title"]
    title.textColor = COLORS["blue"]
    title.fontSize = 28

    story.append(
        Paragraph(
            form.get("name",""),
            title
        )
    )

    story.append(Spacer(1,8))

    contact = f"""
<b>Email:</b> {form.get("email","")}<br/>
<b>Phone:</b> {form.get("country_code","")} {form.get("phone","")}<br/>
<b>GitHub:</b> {form.get("github","")}<br/>
<b>Portfolio:</b> {form.get("portfolio","")}<br/>
<b>LinkedIn:</b> {form.get("linkedin","")}
"""

    add_text(story, contact)

    add_line(story)

    section(
        story,
        "Professional Summary",
        form.get("objective","")
    )

    section(
        story,
        "Technical Skills",
        form.get("technical_skills","")
    )

    section(
        story,
        "Programming Languages",
        form.get("languages_programming","")
    )

    section(
        story,
        "Frameworks",
        form.get("frameworks","")
    )

    section(
        story,
        "Databases",
        form.get("databases","")
    )

    section(
        story,
        "Cloud & DevOps",
        form.get("cloud","")
    )

    section(
        story,
        "Developer Tools",
        form.get("tools","")
    )

    projects_section(story, form)

    experience_section(story, form)

    certification_section(story, form)

    achievement_section(story, form)

    education_section(story, form)

    section(
        story,
        "Coding Profiles",
        form.get("coding_profiles","")
    )

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# DATA SCIENCE / AI TEMPLATE
# =====================================================

def data_science_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "datascience")

    title = styles["Title"]
    title.textColor = COLORS["purple"]
    title.fontSize = 28

    story.append(
        Paragraph(
            form.get("name",""),
            title
        )
    )

    story.append(Spacer(1,8))

    contact = f"""
<b>Email:</b> {form.get("email","")}<br/>
<b>Phone:</b> {form.get("country_code","")} {form.get("phone","")}<br/>
<b>GitHub:</b> {form.get("github","")}<br/>
<b>Kaggle:</b> {form.get("kaggle","")}<br/>
<b>LinkedIn:</b> {form.get("linkedin","")}
"""

    add_text(story, contact)

    add_line(story)

    section(
        story,
        "Professional Summary",
        form.get("objective","")
    )

    section(
        story,
        "Programming Languages",
        form.get("languages_programming","")
    )

    section(
        story,
        "Machine Learning",
        form.get("machine_learning","")
    )

    section(
        story,
        "Deep Learning",
        form.get("deep_learning","")
    )

    section(
        story,
        "Generative AI",
        form.get("genai","")
    )

    section(
        story,
        "Data Visualization",
        form.get("visualization","")
    )

    section(
        story,
        "AI Frameworks",
        form.get("frameworks","")
    )

    section(
        story,
        "Databases",
        form.get("databases","")
    )

    projects_section(story, form)

    experience_section(story, form)

    certification_section(story, form)

    achievement_section(story, form)

    education_section(story, form)

    section(
        story,
        "Research Publications",
        form.get("research","")
    )

    section(
        story,
        "Kaggle Competitions",
        form.get("competitions","")
    )

    document.build(story)

    buffer.seek(0)

    return buffer
  # =====================================================
# CYBER SECURITY TEMPLATE
# =====================================================

def cyber_template(form, files=None):

    document, buffer = create_document()

    story = []

    add_template_photo(story, form, files, "cyber")

    title = styles["Title"]
    title.textColor = COLORS["orange"]
    title.fontSize = 28

    story.append(
        Paragraph(
            form.get("name",""),
            title
        )
    )

    story.append(Spacer(1,8))

    contact = f"""
<b>Email:</b> {form.get("email","")}<br/>
<b>Phone:</b> {form.get("country_code","")} {form.get("phone","")}<br/>
<b>GitHub:</b> {form.get("github","")}<br/>
<b>LinkedIn:</b> {form.get("linkedin","")}
"""

    add_text(story, contact)

    add_line(story)

    section(
        story,
        "Professional Summary",
        form.get("objective","")
    )

    section(
        story,
        "Security Skills",
        form.get("security_skills","")
    )

    section(
        story,
        "Networking",
        form.get("networking","")
    )

    section(
        story,
        "Operating Systems",
        form.get("operating_systems","")
    )

    section(
        story,
        "Penetration Testing",
        form.get("penetration_testing","")
    )

    section(
        story,
        "SIEM Tools",
        form.get("siem","")
    )

    section(
        story,
        "Digital Forensics",
        form.get("forensics","")
    )

    section(
        story,
        "Cloud Security",
        form.get("cloud_security","")
    )

    section(
        story,
        "Security Tools",
        form.get("security_tools","")
    )

    projects_section(story, form)

    experience_section(story, form)

    certification_section(story, form)

    achievement_section(story, form)

    education_section(story, form)

    section(
        story,
        "CTF / Bug Bounty",
        form.get("ctf","")
    )

    section(
        story,
        "Professional Certifications",
        form.get("security_certifications","")
    )

    document.build(story)

    buffer.seek(0)

    return buffer

# =====================================================
# GENERATE RESUME
# =====================================================

def generate_resume(form, files=None):

    template = form.get("template_style", "ats")

    if template == "modern_blue":
        return modern_blue_template(form, files)

    elif template == "professional_black":
        return professional_black_template(form, files)

    elif template == "minimal":
        return minimal_clean_template(form, files)

    elif template == "executive":
        return executive_template(form, files)

    elif template == "creative":
        return creative_template(form, files)

    elif template == "ats":
        return ats_template(form, files)

    elif template == "fresher":
        return fresher_template(form, files)

    elif template == "student":
        return student_template(form, files)

    elif template == "experienced":
        return experienced_template(form, files)

    elif template == "software":
        return software_template(form, files)

    elif template == "datascience":
        return data_science_template(form, files)

    elif template == "cyber":
        return cyber_template(form, files)

    else:
        return ats_template(form, files)
        
