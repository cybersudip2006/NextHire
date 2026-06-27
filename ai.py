import google.generativeai as genai

# =====================================================
# Configure Gemini
# =====================================================

def configure_gemini(api_key):
    """
    Configure Gemini API.
    """

    if not api_key:
        raise ValueError("Gemini API Key not found.")

    genai.configure(api_key=api_key)


# =====================================================
# Load Model
# =====================================================

def get_model():

    return genai.GenerativeModel(
        "models/gemini-2.5-flash"
    )


# =====================================================
# AI Resume Suggestions
# =====================================================

def get_resume_suggestions(api_key, resume_text):

    configure_gemini(api_key)

    model = get_model()

    prompt = f"""

You are a Senior Resume Reviewer.

Analyze the following resume.

Return your answer in Markdown.

Include:

# Professional Summary

# Skills Improvement

# Experience Improvement

# Project Improvement

# Missing ATS Keywords

# Grammar Issues

# Recruiter Tips

Resume:

{resume_text}

"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# ATS ANALYSIS
# =====================================================

def analyze_resume(api_key, resume_text):

    configure_gemini(api_key)

    model = get_model()

    prompt = f"""

You are an ATS Resume Analyzer.

Analyze the following resume.

Return ONLY markdown.

Use this exact structure.

# ATS Score

Give score out of 10.

# Contact Information

Tell whether Name, Email, Phone,
LinkedIn and GitHub exist.

# Missing Keywords

List important missing keywords.

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

Provide detailed improvements.

Resume:

{resume_text}

"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# Rewrite Professional Summary
# =====================================================

def rewrite_summary(api_key, summary):

    configure_gemini(api_key)

    model = get_model()

    prompt = f"""

Rewrite this professional summary.

Make it:

Professional

ATS Friendly

Impactful

Less than 120 words.

Summary:

{summary}

"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# Improve Projects
# =====================================================

def improve_project(api_key, project):

    configure_gemini(api_key)

    model = get_model()

    prompt = f"""

Rewrite this software project.

Use action verbs.

Mention technologies.

Mention measurable impact.

Project:

{project}

"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# Suggest Skills
# =====================================================

def suggest_skills(api_key, domain):

    configure_gemini(api_key)

    model = get_model()

    prompt = f"""

Suggest the top 30 ATS-friendly technical skills
for this career field.

Domain:

{domain}

"""

    response = model.generate_content(prompt)

    return response.text


# =====================================================
# Cover Letter Generator
# =====================================================

def generate_cover_letter(api_key, name, job_role, company):

    configure_gemini(api_key)

    model = get_model()

    prompt = f"""

Write a professional cover letter.

Candidate:

{name}

Job Role:

{job_role}

Company:

{company}

Keep it professional.

"""

    response = model.generate_content(prompt)

    return response.text
