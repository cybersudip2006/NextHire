```python
import os
import pdfplumber

from flask import Flask, render_template, request, send_file, redirect

from config import Config
from models import db, ResumeData
from pdf_generator import generate_resume
from ai import analyze_resume, get_resume_suggestions
from ats import calculate_ats


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
        name = request.form.get("name", "")[:100]
        email = request.form.get("email", "")
        phone_code = request.form.get("country_code", "")
        phone_num = request.form.get("phone", "")
        full_phone = f"{phone_code} {phone_num}".strip()

        if name and email and phone_num:
            new_resume = ResumeData(
                name=name,
                email=email,
                phone=full_phone
            )
            db.session.add(new_resume)
            db.session.commit()

        pdf_buffer = generate_resume(request.form)

        safe_name = name.replace(" ", "_") if name else "NextHire"

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{safe_name}_Resume.pdf",
            mimetype="application/pdf"
        )

    return render_template("builder.html")


@app.route("/ats-checker", methods=["GET", "POST"])
def ats_checker():
    results = None

    if request.method == "POST":
        if "resume_pdf" not in request.files:
            return redirect(request.url)

        file = request.files["resume_pdf"]

        if file.filename != "":
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

                    ai_feedback = analyze_resume(
                        app.config["GEMINI_API_KEY"],
                        text[:app.config.get("ATS_MAX_RESUME_CHARS", 15000)]
                    )

                    results = {
                        "score": local_result["ats_score"],
                        "contact": local_result["contact"],
                        "sections": local_result["sections"],
                        "keywords_found": local_result["found_keywords"],
                        "keywords_missing": local_result["missing_keywords"],
                        "skill_score": local_result["skill_score"],
                        "education_score": local_result["education_score"],
                        "experience_score": local_result["experience_score"],
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
        text_input = request.form.get("resume_text", "")

        if not text_input or len(text_input.strip()) < 20:
            return render_template(
                "ai_suggestions.html",
                suggestions=["Please enter a longer resume text, at least 20 characters."]
            )

        try:
            response = get_resume_suggestions(
                app.config["GEMINI_API_KEY"],
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
    app.run(debug=True)
```
