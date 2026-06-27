import json
import re
import google.generativeai as genai


GEMINI_MODEL = "models/gemini-2.5-flash"


def configure_gemini(api_key):
    if not api_key:
        raise ValueError("Gemini API Key not found.")
    genai.configure(api_key=api_key)


def get_model():
    return genai.GenerativeModel(GEMINI_MODEL)


def _generate(api_key, prompt):
    configure_gemini(api_key)
    model = get_model()
    response = model.generate_content(prompt)
    return response.text if hasattr(response, "text") else "No AI response received."


def _clean_json_text(text):
    if not text:
        return ""

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()

    # Extract from first { to last }
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)

    # Replace smart quotes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")

    return text


def extract_json(text):
    """
    Robust JSON extraction:
    1. Try direct JSON
    2. Try cleaned JSON
    3. Try markdown fenced JSON
    4. Return {} if impossible
    """

    if not text:
        return {}

    candidates = []

    candidates.append(text.strip())
    candidates.append(_clean_json_text(text))

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        candidates.append(_clean_json_text(fenced.group(1)))

    for candidate in candidates:
        if not candidate:
            continue

        try:
            return json.loads(candidate)
        except Exception:
            continue

    return {}


def extract_score_from_text(text):
    """
    Fallback parser if Gemini returns markdown instead of JSON.
    """

    if not text:
        return {}

    def find_number(pattern, default=0):
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return default
        try:
            return float(match.group(1))
        except Exception:
            return default

    ats_score = find_number(r"ATS\s*Score[^0-9]*(\d+(?:\.\d+)?)", 0)
    keyword_match = find_number(r"Keyword\s*Match[^0-9]*(\d+(?:\.\d+)?)", 0)
    interview_chance = find_number(r"Interview\s*Chance[^0-9]*(\d+(?:\.\d+)?)", 0)

    # Extract bullet-like missing keywords
    missing_keywords = []
    missing_section = re.search(
        r"Missing[^#]*Keywords(.*?)(?:\n#|\n[A-Z][A-Za-z ]{3,}:|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if missing_section:
        lines = missing_section.group(1).splitlines()
        for line in lines:
            line = line.strip(" -*•\t")
            if line and len(line) < 60:
                missing_keywords.append(line)

    return {
        "ats_score": ats_score,
        "keyword_match": keyword_match,
        "interview_chance": interview_chance,
        "missing_keywords": missing_keywords[:20],
        "deep_analysis": text
    }


def ensure_ai_schema(data, raw_text="", job_role=""):
    """
    Guarantees every field exists even if Gemini output is incomplete.
    """

    if not isinstance(data, dict):
        data = {}

    fallback = extract_score_from_text(raw_text)

    def num(key, default=0):
        value = data.get(key, fallback.get(key, default))
        try:
            return float(value)
        except Exception:
            return default

    def arr(key):
        value = data.get(key, fallback.get(key, []))
        return value if isinstance(value, list) else []

    def txt(key, default=""):
        value = data.get(key, fallback.get(key, default))
        return value if isinstance(value, str) else default

    return {
        "target_role": txt("target_role", job_role),
        "ats_score": num("ats_score"),
        "skills_score": num("skills_score"),
        "education_score": num("education_score"),
        "experience_score": num("experience_score"),
        "projects_score": num("projects_score"),
        "format_score": num("format_score"),
        "keyword_match": num("keyword_match"),
        "interview_chance": num("interview_chance"),
        "found_keywords": arr("found_keywords"),
        "missing_keywords": arr("missing_keywords"),
        "strengths": arr("strengths"),
        "weaknesses": arr("weaknesses"),
        "recommendations": arr("recommendations"),
        "job_fit_summary": txt("job_fit_summary", ""),
        "recruiter_opinion": txt("recruiter_opinion", ""),
        "deep_analysis": txt("deep_analysis", raw_text)
    }


def analyze_resume_json(api_key, resume_text, job_role="", job_description=""):
    job_role = job_role or "General Job Role"
    job_description = job_description or "No job description provided. Analyze based on the target role and common industry expectations."

    prompt = f"""
You are an expert ATS system and senior recruiter.

Analyze this resume specifically for this target job role:

TARGET JOB ROLE:
{job_role}

JOB DESCRIPTION / REQUIRED SKILLS:
{job_description}

RESUME TEXT:
{resume_text}

Return RAW JSON ONLY.
No markdown.
No ```json.
No explanation outside JSON.
The first character must be {{ and the last character must be }}.

Use exactly this JSON structure:

{{
  "target_role": "{job_role}",
  "ats_score": 0,
  "skills_score": 0,
  "education_score": 0,
  "experience_score": 0,
  "projects_score": 0,
  "format_score": 0,
  "keyword_match": 0,
  "interview_chance": 0,
  "found_keywords": [],
  "missing_keywords": [],
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "job_fit_summary": "",
  "recruiter_opinion": "",
  "deep_analysis": ""
}}

Rules:
- Scores must be numbers out of 10 except keyword_match and interview_chance, which are percentages from 0 to 100.
- Found keywords must come from the resume and be relevant to the target role/job description.
- Missing keywords must be relevant to the target role/job description.
- Do not use a generic fixed keyword list.
- If job description is provided, compare resume directly against it.
- If job description is not provided, infer realistic keywords from the target role.
- If skills are missing, skills_score should be low, not a default score.
- If education is missing, education_score should be low.
- If experience/projects are missing, score accordingly.
"""

    raw_response = _generate(api_key, prompt)

    data = extract_json(raw_response)

    # If Gemini still returns text, fallback parser fills whatever it can.
    return ensure_ai_schema(data, raw_response, job_role)


def analyze_resume(api_key, resume_text, job_role="", job_description=""):
    job_role = job_role or "General Job Role"
    job_description = job_description or "No job description provided."

    prompt = f"""
You are an expert ATS resume analyzer and recruiter.

Analyze the resume for this target role:

Target Job Role:
{job_role}

Job Description / Required Skills:
{job_description}

Return Markdown using this structure:

# ATS Score
# Target Role Fit
# Found Role-Specific Keywords
# Missing Role-Specific Keywords
# Skills Gap
# Experience Gap
# Projects Gap
# Education Fit
# Formatting
# Recruiter Opinion
# Interview Chance
# Final Suggestions

Resume:
{resume_text}
"""

    return _generate(api_key, prompt)


def rewrite_resume_section(api_key, resume_text, job_role="", section_type="summary"):
    section_labels = {
        "summary": "Professional Summary",
        "experience": "Experience",
        "projects": "Projects",
        "skills": "Skills",
        "education": "Education",
        "full": "Entire Resume"
    }

    section_name = section_labels.get(section_type, "Professional Summary")
    job_role = job_role or "General Job Role"

    prompt = f"""
You are a professional resume writer and ATS optimization expert.

Target Job Role:
{job_role}

Task:
Rewrite ONLY this resume section: {section_name}

Resume Text:
{resume_text}

Rules:
- Make it ATS-friendly.
- Use role-specific keywords naturally.
- Use strong action verbs.
- Use measurable impact where possible.
- Do not invent fake companies, fake degrees, fake certificates, or fake achievements.
- If details are missing, write a polished version using only available information.
- Keep it concise and recruiter-friendly.
- Return only the rewritten content.
- Do not add markdown heading unless rewriting the entire resume.
"""

    if section_type == "full":
        prompt += """
For the full resume rewrite, return a clean resume structure with these headings where relevant:
Professional Summary
Skills
Experience
Projects
Education
Certifications
Achievements
"""

    return _generate(api_key, prompt)


def get_resume_suggestions(api_key, resume_text):
    prompt = f"""
You are a senior resume reviewer.

Analyze this resume and return Markdown with:

# Professional Summary
# Skills Improvement
# Experience Improvement
# Project Improvement
# Missing ATS Keywords
# Grammar Issues
# Recruiter Tips
# Final Action Plan

Resume:
{resume_text}
"""
    return _generate(api_key, prompt)


def rewrite_summary(api_key, summary):
    return _generate(api_key, f"Rewrite this professional summary to be ATS-friendly and under 120 words:\n\n{summary}")


def improve_project(api_key, project):
    return _generate(api_key, f"Rewrite this project using action verbs, technologies, and measurable impact:\n\n{project}")


def suggest_skills(api_key, domain):
    return _generate(api_key, f"Suggest the top 30 ATS-friendly technical skills for this career field:\n\n{domain}")


def match_job_description(api_key, resume_text, job_description):
    prompt = f"""
Compare this resume against the job description.

Return:
- Match percentage
- Missing keywords
- Skills to add
- Summary rewrite
- Project improvements
- Final action plan

Resume:
{resume_text}

Job Description:
{job_description}
"""
    return _generate(api_key, prompt)


def generate_cover_letter(api_key, name, job_role, company):
    return _generate(api_key, f"Write a professional cover letter. Candidate: {name}. Job Role: {job_role}. Company: {company}.")
