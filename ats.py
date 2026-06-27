import re
from collections import Counter

COMMON_KEYWORDS = [
    "python", "java", "c", "c++", "sql", "mysql", "mongodb", "html", "css",
    "javascript", "react", "node", "flask", "django", "git", "github",
    "linux", "aws", "azure", "docker", "kubernetes", "api", "rest",
    "machine learning", "artificial intelligence", "deep learning",
    "data science", "cyber security", "network", "communication",
    "leadership", "problem solving", "teamwork", "critical thinking",
    "database", "cloud", "security", "analytics", "automation"
]

ACTION_VERBS = [
    "built", "developed", "created", "implemented", "designed", "managed",
    "led", "optimized", "improved", "analyzed", "secured", "deployed",
    "automated", "integrated", "tested", "monitored"
]


def normalize(text):
    return text.lower() if text else ""


def check_contact(text):
    lower = normalize(text)

    return {
        "email": bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)),
        "phone": bool(re.search(r"\+?\d[\d\s\-]{8,}", text)),
        "linkedin": "linkedin" in lower,
        "github": "github" in lower
    }


def check_sections(text):
    lower = normalize(text)

    return {
        "education": "education" in lower,
        "experience": any(word in lower for word in ["experience", "internship", "employment", "work history"]),
        "skills": "skills" in lower,
        "projects": "project" in lower,
        "certifications": any(word in lower for word in ["certification", "certifications", "certificate"]),
        "summary": any(word in lower for word in ["summary", "objective", "profile"])
    }


def keyword_analysis(text):
    lower = normalize(text)

    found = []
    missing = []

    for word in COMMON_KEYWORDS:
        if word in lower:
            found.append(word)
        else:
            missing.append(word)

    return found, missing


def formatting_score(text):
    score = 10
    length = len(text.split())

    if length < 150:
        score -= 3

    if length > 900:
        score -= 1

    if not re.search(r"[-•]", text):
        score -= 1

    if text.count("\n") < 5:
        score -= 1

    return max(0, min(score, 10))


def action_verb_score(text):
    lower = normalize(text)
    found = [verb for verb in ACTION_VERBS if verb in lower]

    if len(found) >= 8:
        return 10

    if len(found) >= 5:
        return 8

    if len(found) >= 3:
        return 6

    return 4


def education_score(text):
    lower = normalize(text)

    keywords = ["b.tech", "btech", "bachelor", "diploma", "college", "cgpa", "school", "university"]
    score = sum(2 for item in keywords if item in lower)

    return min(score, 10)


def experience_score(text):
    lower = normalize(text)

    score = 0

    if "experience" in lower:
        score += 2

    if "internship" in lower:
        score += 2

    if "project" in lower:
        score += 2

    if "achievement" in lower:
        score += 2

    if re.search(r"\d+%|\d+\+", lower):
        score += 2

    return min(score, 10)


def skills_score(found_keywords):
    count = len(found_keywords)

    if count >= 20:
        return 10

    if count >= 15:
        return 9

    if count >= 10:
        return 8

    if count >= 8:
        return 7

    if count >= 5:
        return 6

    return 4


def get_strengths(contact, sections, found_keywords):
    strengths = []

    if contact["email"] and contact["phone"]:
        strengths.append("Contact details are present.")

    if sections["projects"]:
        strengths.append("Project section is available.")

    if sections["skills"]:
        strengths.append("Skills section is available.")

    if len(found_keywords) >= 8:
        strengths.append("Good keyword coverage.")

    return strengths or ["Resume has basic structure."]


def get_weaknesses(contact, sections, missing_keywords):
    weaknesses = []

    if not contact["linkedin"]:
        weaknesses.append("LinkedIn profile is missing.")

    if not contact["github"]:
        weaknesses.append("GitHub link is missing.")

    for section, present in sections.items():
        if not present:
            weaknesses.append(f"{section.title()} section may be missing.")

    if missing_keywords:
        weaknesses.append("Important ATS keywords are missing.")

    return weaknesses


def calculate_ats(text):
    text = text or ""

    contact = check_contact(text)
    sections = check_sections(text)
    found, missing = keyword_analysis(text)

    skill = skills_score(found)
    edu = education_score(text)
    exp = experience_score(text)
    fmt = formatting_score(text)
    verbs = action_verb_score(text)

    contact_score = sum(contact.values()) / 4 * 10
    section_score = sum(sections.values()) / len(sections) * 10

    final = round(
        (
            contact_score * 0.15
            + section_score * 0.20
            + skill * 0.20
            + edu * 0.10
            + exp * 0.15
            + fmt * 0.10
            + verbs * 0.10
        ),
        1
    )

    return {
        "ats_score": final,
        "contact": contact,
        "sections": sections,
        "found_keywords": found,
        "missing_keywords": missing[:25],
        "skill_score": skill,
        "education_score": edu,
        "experience_score": exp,
        "format_score": fmt,
        "action_verb_score": verbs,
        "strengths": get_strengths(contact, sections, found),
        "weaknesses": get_weaknesses(contact, sections, missing[:8]),
        "recommendations": [
            "Add measurable achievements using numbers or percentages.",
            "Include role-specific keywords from the job description.",
            "Keep section headings clear and ATS-readable.",
            "Add GitHub, LinkedIn, and project links where possible."
        ]
    }
