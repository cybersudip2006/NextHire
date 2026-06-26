import os
import io
import re
from flask import Flask, render_template, request, send_file, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pdfplumber

app = Flask(__name__)
# Uses environment variable for production, fallback for local
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "nexthire_super_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexthire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class ResumeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/builder', methods=['GET', 'POST'])
def builder():
    if request.method == 'POST':
        # Apply strict limits requested (100 for name, 250 for address)
        name = request.form.get('name')[:100] 
        email = request.form.get('email')
        phone_code = request.form.get('country_code', '')
        phone_num = request.form.get('phone', '')
        full_phone = f"{phone_code} {phone_num}"
        address = request.form.get('address')[:250] 
        objective = request.form.get('objective', '')
        
        # Save to DB
        new_resume = ResumeData(name=name, email=email, phone=full_phone)
        db.session.add(new_resume)
        db.session.commit()

        # Generate PDF
        return generate_pdf(name, email, full_phone, address, objective, request.form)
        
    return render_template('builder.html')

@app.route('/ats-checker', methods=['GET', 'POST'])
def ats_checker():
    results = None
    if request.method == 'POST':
        if 'resume_pdf' not in request.files:
            return redirect(request.url)
        
        file = request.files['resume_pdf']
        if file.filename != '':
            # Extract text from PDF
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            
            # --- GEMINI AI ANALYSIS ---
            import google.generativeai as genai
            api_key = os.environ.get("GEMINI_API_KEY")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
prompt = f"""
Act as an expert ATS (Applicant Tracking System) recruiter. 
Analyze the following resume text and provide a comprehensive report.

Use Markdown formatting:
- Use ### for section titles.
- Use **bold** for key terms or scores.
- Use - for bullet points.

Please include:
1. An ATS compatibility score (0-100).
2. A list of missing keywords for a professional tech role.
3. A brief critique of the formatting and content.
4. 3 specific, actionable improvements.

Resume Text: {text[:15000]}
"""
            
            response = model.generate_content(prompt)
            
            # Here we pass the AI's raw response to the template
            results = {
                "ai_feedback": response.text
            }
            
    return render_template('ats_checker.html', results=results)

@app.route('/ai-suggestions', methods=['GET', 'POST'])
def ai_suggestions():
    suggestions = None
    if request.method == 'POST':
        text_input = request.form.get('resume_text')
        
        # 1. Fetch the secret key
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # 2. Initialize and configure the real Gemini model
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze this resume text and provide 3-5 concise, bullet-point suggestions for improvement: {text_input}"
        
        response = model.generate_content(prompt)
        
        # 3. Clean up the response
        suggestions = [line.strip('* ').strip('- ') for line in response.text.split('\n') if line.strip()]
        
    return render_template('ai_suggestions.html', suggestions=suggestions)
    
# --- PDF GENERATOR (No QR Code) ---
def generate_pdf(name, email, phone, address, objective, form):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Modern UI Layout
    c.setFillColorRGB(0.95, 0.97, 1.0) # Light blue header
    c.rect(0, height - 120, width, 120, fill=1, stroke=0)
    
    # Header Text
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(50, height - 50, name)
    
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 75, f"{email} | {phone}")
    c.drawString(50, height - 90, address)
    
    # Objective
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 150, "Professional Objective")
    c.setFont("Helvetica", 11)
    
    # Text wrapping simulation for objective
    y_pos = height - 170
    c.drawString(50, y_pos, objective[:120])
    
    # Education
    edu_school = form.get('edu_school', '')
    if edu_school:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_pos - 40, "Education")
        c.setFont("Helvetica", 11)
        edu_start = form.get('edu_start', '')
        edu_end = form.get('edu_end', '')
        dates = f" ({edu_start} - {edu_end})" if edu_start or edu_end else ""
        c.drawString(50, y_pos - 60, f"{edu_school}{dates}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{name.replace(' ', '_')}_Resume.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
