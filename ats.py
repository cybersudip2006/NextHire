import re


def normalize(text):
    return text.lower() if text else ""


def check_contact(text):
    lower = normalize(text)
    return {
        "email": bool(re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or "")),
        "phone": bool(re.search(r"\+?\d[\d\s\-]{8,}", text or "")),
        "linkedin": "linkedin" in lower,
        "github": "github" in lower
    }


def check_sections(text):
    lower = normalize(text)
    return {
        "summary": any(word in lower for word in ["summary", "objective", "profile"]),
        "skills": "skills" in lower,
        "education": "education" in lower,
        "experience": any(word in lower for word in ["experience", "internship", "employment", "work history"]),
        "projects": "project" in lower,
        "certifications": any(word in lower for word in ["certification", "certifications", "certificate"])
    }


def calculate_basic_ats(text):
    text = text or ""
    contact = check_contact(text)
    sections = check_sections(text)
    return {
        "contact": contact,
        "sections": sections,
        "contact_score": round(sum(contact.values()) / len(contact) * 10, 1),
        "section_score": round(sum(sections.values()) / len(sections) * 10, 1)
    }


def safe_float(value, default=0):
    try:
        return float(value)
    except Exception:
        return default


def normalize_ai_result(data):
    if not isinstance(data, dict):
        data = {}

    return {
        "ats_score": safe_float(data.get("ats_score", 0)),
        "skills_score": safe_float(data.get("skills_score", 0)),
        "education_score": safe_float(data.get("education_score", 0)),
        "experience_score": safe_float(data.get("experience_score", 0)),
        "projects_score": safe_float(data.get("projects_score", 0)),
        "format_score": safe_float(data.get("format_score", 0)),
        "keyword_match": safe_float(data.get("keyword_match", 0)),
        "interview_chance": safe_float(data.get("interview_chance", 0)),
        "target_role": data.get("target_role", ""),
        "found_keywords": data.get("found_keywords", []) if isinstance(data.get("found_keywords", []), list) else [],
        "missing_keywords": data.get("missing_keywords", []) if isinstance(data.get("missing_keywords", []), list) else [],
        "strengths": data.get("strengths", []) if isinstance(data.get("strengths", []), list) else [],
        "weaknesses": data.get("weaknesses", []) if isinstance(data.get("weaknesses", []), list) else [],
        "recommendations": data.get("recommendations", []) if isinstance(data.get("recommendations", []), list) else [],
        "job_fit_summary": data.get("job_fit_summary", ""),
        "recruiter_opinion": data.get("recruiter_opinion", ""),
        "deep_analysis": data.get("deep_analysis", "")
    }
