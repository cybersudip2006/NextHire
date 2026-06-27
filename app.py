import os
import pdfplumber

from flask import Flask, render_template, request, send_file, redirect

from config import Config
from models import db, ResumeData
from pdf_generator import generate_resume
from ai import analyze_resume, get_resume_suggestions
from ats import calculate_ats
from utils import resume_filename


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/builder", methods=["GET", "POST"])
def builder():
    if request.method == "POST":
        name = request.form.get("name", "").strip()[: app.config.get("MAX_NAME_LENGTH", 100)]
        email = request.form.get("email", "").strip()
        phone_code = request.form.get("country_code", "").strip()
        phone_num = request.form.get("phone", "").strip()
        full_phone = f"{phone_code} {phone_num}".strip()
        template_style = request.form.get("template_style", app.config.get("DEFAULT_TEMPLATE", "ats"))

        try:
            if name and email and phone_num:
                new_resume = ResumeData(
                    name=name,
                    email=email,
                    phone=full_phone,
                    template_style=template_style,
                    filename=resume_filename(name)
                )

                db.session.add(new_resume)
                db.session.commit()

        except Exception:
            db.session.rollback()

        try:
            pdf_buffer = generate_resume(request.form)

            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=resume_filename(name),
                mimetype="application/pdf"
            )

        except Exception as e:
            return f"Resume generation error: {str(e)}", 500

    return render_template("builder.html")


@app.route("/ats-checker", methods=["GET", "POST"])
def ats_checker():
    results = None

    if request.method == "POST":
        if "resume_pdf" not in request.files:
            return redirect(request.url)

        file = request.files["resume_pdf"]

        if file.filename == "":
            return redirect(request.url)

        try:
            text = ""

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"

            if not text.strip():
                results = {
                    "ai_feedback": "Error: Could not read text from this PDF. Please upload a text-based PDF."
                }

            else:
                local_result = calculate_ats(text)

                api_key = app.config.get("GEMINI_API_KEY")

                if api_key:
                    ai_feedback = analyze_resume(
                        api_key,
                        text[: app.config.get("ATS_MAX_RESUME_CHARS", 15000)]
                    )
                else:
                    ai_feedback = "Gemini API key is not configured. Local ATS analysis completed."

                results = {
                    "score": local_result.get("ats_score"),
                    "contact": local_result.get("contact", {}),
                    "sections": local_result.get("sections", {}),
                    "keywords_found": local_result.get("found_keywords", []),
                    "keywords_missing": local_result.get("missing_keywords", []),
                    "skill_score": local_result.get("skill_score"),
                    "education_score": local_result.get("education_score"),
                    "experience_score": local_result.get("experience_score"),
                    "format_score": local_result.get("format_score"),
                    "action_verb_score": local_result.get("action_verb_score"),
                    "strengths": local_result.get("strengths", []),
                    "weaknesses": local_result.get("weaknesses", []),
                    "recommendations": local_result.get("recommendations", []),
                    "ai_feedback": ai_feedback
                }

        except Exception as e:
            results = {
                "ai_feedback": f"System Error during analysis: {str(e)}"
            }

    return render_template("ats_checker.html", results=results)


@app.route("/ai-suggestions", methods=["GET", "POST"])
def ai_suggestions():
    suggestions = None

    if request.method == "POST":
        text_input = request.form.get("resume_text", "").strip()

        if not text_input or len(text_input) < 20:
            return render_template(
                "ai_suggestions.html",
                suggestions=["Please enter a longer resume text, at least 20 characters."]
            )

        try:
            api_key = app.config.get("GEMINI_API_KEY")

            if not api_key:
                suggestions = ["Gemini API key is not configured on the server."]

            else:
                response = get_resume_suggestions(
                    api_key,
                    text_input
                )

                suggestions = [
                    line.strip()
                    for line in response.split("\n")
                    if line.strip()
                ]

        except Exception as e:
            suggestions = [f"System Error: {str(e)}"]

    return render_template("ai_suggestions.html", suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=False)
