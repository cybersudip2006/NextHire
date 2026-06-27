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


def extract_json(text):
    if not text:
        return {}

    text = text.strip()

    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if code_block:
        text = code_block.group(1)

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            return {}

    return {}


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

Return ONLY valid JSON.
Do not use markdown.
Do not add explanation outside JSON.

Use this exact JSON structure:

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

    response_text = _generate(api_key, prompt)
    return extract_json(response_text)


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
