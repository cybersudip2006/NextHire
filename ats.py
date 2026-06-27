import re

# ==========================================================
# ATS KEYWORDS DATABASE
# ==========================================================

COMMON_KEYWORDS = [

    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "html",
    "css",
    "javascript",
    "react",
    "node",
    "flask",
    "django",
    "git",
    "github",
    "linux",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "api",
    "rest",
    "machine learning",
    "artificial intelligence",
    "deep learning",
    "data science",
    "cyber security",
    "network",
    "communication",
    "leadership",
    "problem solving",
    "teamwork",
    "critical thinking"

]


# ==========================================================
# CHECK CONTACT DETAILS
# ==========================================================

def check_contact(text):

    result = {}

    result["email"] = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    result["phone"] = bool(
        re.search(
            r"\+?\d[\d\s\-]{8,}",
            text
        )
    )

    result["linkedin"] = "linkedin" in text.lower()

    result["github"] = "github" in text.lower()

    return result


# ==========================================================
# CHECK SECTIONS
# ==========================================================

def check_sections(text):

    lower = text.lower()

    sections = {

        "education": "education" in lower,

        "experience":
            ("experience" in lower)
            or ("internship" in lower)
            or ("employment" in lower),

        "skills":
            "skills" in lower,

        "projects":
            "projects" in lower,

        "certifications":
            "certification" in lower
            or "certifications" in lower,

        "objective":
            "objective" in lower
            or "summary" in lower

    }

    return sections


# ==========================================================
# CHECK ATS KEYWORDS
# ==========================================================

def keyword_analysis(text):

    lower = text.lower()

    found = []

    missing = []

    for word in COMMON_KEYWORDS:

        if word in lower:
            found.append(word)
        else:
            missing.append(word)

    return found, missing


# ==========================================================
# EXPERIENCE CHECK
# ==========================================================

def experience_score(text):

    lower = text.lower()

    score = 0

    if "experience" in lower:
        score += 2

    if "internship" in lower:
        score += 2

    if "project" in lower:
        score += 2

    if "achievement" in lower:
        score += 2

    if "%" in lower:
        score += 2

    return min(score,10)


# ==========================================================
# EDUCATION CHECK
# ==========================================================

def education_score(text):

    lower = text.lower()

    score = 0

    keywords = [

        "b.tech",
        "btech",
        "bachelor",
        "college",
        "cgpa",
        "school",
        "university"

    ]

    for item in keywords:

        if item in lower:

            score += 2

    return min(score,10)


# ==========================================================
# SKILLS SCORE
# ==========================================================

def skills_score(found_keywords):

    if len(found_keywords) >= 20:
        return 10

    if len(found_keywords) >= 15:
        return 9

    if len(found_keywords) >= 10:
        return 8

    if len(found_keywords) >= 8:
        return 7

    if len(found_keywords) >= 5:
        return 6

    return 4


# ==========================================================
# OVERALL ATS SCORE
# ==========================================================

def calculate_ats(text):

    contact = check_contact(text)

    sections = check_sections(text)

    found, missing = keyword_analysis(text)

    skill = skills_score(found)

    edu = education_score(text)

    exp = experience_score(text)

    score = 0

    if contact["email"]:
        score += 1

    if contact["phone"]:
        score += 1

    if contact["linkedin"]:
        score += 1

    if contact["github"]:
        score += 1

    score += skill

    score += edu

    score += exp

    score += sum(sections.values())

    max_score = 40

    final = round((score/max_score)*10,1)

    return {

        "ats_score": final,

        "contact": contact,

        "sections": sections,

        "found_keywords": found,

        "missing_keywords": missing[:25],

        "skill_score": skill,

        "education_score": edu,

        "experience_score": exp

    }
