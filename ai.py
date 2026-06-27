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


def analyze_resume(api_key, resume_text):
    prompt = f"""
You are an expert ATS resume analyzer.

Return ONLY Markdown using this exact structure:

# ATS Score
Give score out of 10.

# Contact Information
Check Name, Email, Phone, LinkedIn, GitHub.

# Missing Keywords
List missing keywords.

# Formatting
Explain formatting problems.

# Skills
Analyze skills.

# Experience
Analyze experience.

# Education
Analyze education.

# Recruiter Opinion
Would you shortlist this candidate?

# Interview Chance
Give percentage.

# Final Suggestions
Give detailed improvements.

Resume:
{resume_text}
"""
    return _generate(api_key, prompt)


def rewrite_summary(api_key, summary):
    prompt = f"""
Rewrite this professional summary to be professional, ATS-friendly,
impactful, and less than 120 words.

Summary:
{summary}
"""
    return _generate(api_key, prompt)


def improve_project(api_key, project):
    prompt = f"""
Rewrite this project using action verbs, technologies, and measurable impact.

Project:
{project}
"""
    return _generate(api_key, prompt)


def suggest_skills(api_key, domain):
    prompt = f"""
Suggest the top 30 ATS-friendly technical skills for this career field:

{domain}
"""
    return _generate(api_key, prompt)


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
    prompt = f"""
Write a professional cover letter.

Candidate: {name}
Job Role: {job_role}
Company: {company}

Keep it concise and professional.
"""
    return _generate(api_key, prompt)
