from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import pandas as pd
import pickle
import os
from docx import Document
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from google import genai


# =========================
# PROJECT PATH CONFIGURATION
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
USERS_FILE = os.path.join(BASE_DIR, "users.json")


# =========================
# FLASK APP CONFIGURATION
# =========================

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "temporary-development-secret-key"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================
# GEMINI CONFIGURATION
# =========================

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("Warning: GEMINI_API_KEY is missing from the .env file.")

gemini_client = genai.Client(api_key=gemini_api_key)


# =========================
# USER FILE FUNCTIONS
# =========================

def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


# =========================
# RESUME TEXT EXTRACTION
# =========================

def extract_text_from_docx(file_path):
    document = Document(file_path)
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + " "

    return text.lower()


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text.lower()


# =========================
# ROUTES START HERE
# =========================


#HOME
@app.route('/')
def home():
    return render_template("index.html")



# REGISTER
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()

        if email in users:
            return "User already exists"

        users[email] = {
            "name": name,
            "password": password
        }

        save_users(users)

        return redirect(url_for("login"))

    return render_template("register.html")

# LOGIN
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        print("LOGIN ATTEMPT:", email, password)

        users = load_users()
        print("USERS:", users)

        if email in users and users[email]["password"] == password:
            print("LOGIN SUCCESS")
            session["user"] = users[email]["name"]
            return redirect(url_for("dashboard"))

        print("LOGIN FAILED")
        return "Invalid Credentials"

    return render_template("login.html")

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", name=session["user"])


@app.route('/career')
def career():
    if "user" not in session:
        return redirect(url_for("login"))

    streams = sorted(df["Stream"].dropna().unique())
    technical_skills = sorted(df["Technical Skill"].dropna().unique())
    soft_skills = sorted(df["Soft Skill"].dropna().unique())
    personalities = sorted(df["Personality"].dropna().unique())
    interests = sorted(df["Interest"].dropna().unique())
    work_styles = sorted(df["Work Style"].dropna().unique())

    return render_template(
        "career.html",
        streams=streams,
        technical_skills=technical_skills,
        soft_skills=soft_skills,
        personalities=personalities,
        interests=interests,
        work_styles=work_styles
    )

# LOGOUT
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

df = pd.read_csv(os.path.join(BASE_DIR, "Dataset.csv"))

with open(os.path.join(BASE_DIR, "career_model.pkl"), "rb") as file:
    career_model = pickle.load(file)

with open(os.path.join(BASE_DIR, "target_encoder.pkl"), "rb") as file:
    target_encoder = pickle.load(file)


@app.route("/career-match", methods=["POST"])
def career_match():

    data = request.get_json()

    input_data = pd.DataFrame([{
        "Academic Score": float(data["academic_score"]),
        "Stream": data["stream"],
        "Technical Skill": data["technical_skill"],
        "Soft Skill": data["soft_skill"],
        "Personality": data["personality"],
        "Interest": data["interest"],
        "Work Style": data["work_style"]
    }])

    probabilities = career_model.predict_proba(input_data)[0]

    top_indices = probabilities.argsort()[-3:][::-1]

    recommendations = []

    for index in top_indices:

        career = str(target_encoder.inverse_transform([int(index)])[0])

        match = float(round(float(probabilities[index]) * 100, 2))

        recommendations.append({
            "career": career,
            "match": match,
            "reason": "Prediction generated using XGBoost model trained on academic, skill, personality, interest and work-style features."
        })

    return jsonify({
        "recommendations": recommendations
    })

@app.route('/skill-analysis')
def skill_analysis():
    if "user" not in session:
        return redirect(url_for("login"))

    careers = sorted(df["Career Domain"].dropna().unique())
    technical_skills = sorted(df["Technical Skill"].dropna().unique())
    soft_skills = sorted(df["Soft Skill"].dropna().unique())

    return render_template(
        "skill_analysis.html",
        careers=careers,
        technical_skills=technical_skills,
        soft_skills=soft_skills
    )


@app.route("/analyze-skill-gap", methods=["POST"])
def analyze_skill_gap():
    data = request.get_json()

    target_career = data["target_career"].strip().lower()
    current_technical_skill = data["current_technical_skill"].strip().lower()
    current_soft_skill = data["current_soft_skill"].strip().lower()

    career_rows = df[df["Career Domain"].str.lower() == target_career]

    if career_rows.empty:
        return jsonify({"error": "Career not found"})

    required_technical = career_rows["Technical Skill"].mode()[0]
    required_soft = career_rows["Soft Skill"].mode()[0]

    matched_skills = []
    missing_skills = []

    if current_technical_skill == required_technical.lower():
        matched_skills.append(required_technical)
    else:
        missing_skills.append(required_technical)

    if current_soft_skill == required_soft.lower():
        matched_skills.append(required_soft)
    else:
        missing_skills.append(required_soft)

    match_score = round((len(matched_skills) / 2) * 100)

    return jsonify({
        "target_career": target_career.title(),
        "match_score": match_score,
        "matched_count": len(matched_skills),
        "missing_count": len(missing_skills),
        "learning_count": len(missing_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_overview": [
            {"skill": current_technical_skill.title(), "status": "Good" if current_technical_skill == required_technical.lower() else "Major Gap"},
            {"skill": current_soft_skill.title(), "status": "Good" if current_soft_skill == required_soft.lower() else "Moderate"},
            {"skill": required_technical, "status": "Required Skill"},
            {"skill": required_soft, "status": "Required Soft Skill"}
        ],
        "recommendation": f"To improve for {target_career.title()}, focus on {', '.join(missing_skills) if missing_skills else 'advanced projects and interview preparation'}."
    })

@app.route('/learning-roadmap')
def learning_roadmap():
    if "user" not in session:
        return redirect(url_for("login"))

    careers = sorted(df["Career Domain"].dropna().unique())

    return render_template(
        "learning_roadmap.html",
        careers=careers
    )

# ===================== LEARNING ROADMAP =====================

@app.route("/generate-roadmap", methods=["POST"])
def generate_roadmap():

    data = request.get_json()
    target_career = data["target_career"]

    career_rows = df[df["Career Domain"].str.lower() == target_career.lower()]

    if career_rows.empty:
        return jsonify({
            "error": "Career not found"
        })

    required_technical = career_rows["Technical Skill"].mode()[0]
    required_soft = career_rows["Soft Skill"].mode()[0]
    interest = career_rows["Interest"].mode()[0]

    roadmap_library = {

        "Python": {
            "courses": [
                "Python Fundamentals",
                "Object-Oriented Programming",
                "Data Structures in Python",
                "Machine Learning with Python"
            ],
            "certifications": [
                "Python Institute PCEP",
                "Google Python Certificate"
            ],
            "projects": [
                "Student Management System",
                "AI Career Guidance System",
                "Data Analysis Dashboard"
            ]
        },

        "SQL": {
            "courses": [
                "SQL Basics",
                "Advanced SQL",
                "Database Design",
                "MySQL Projects"
            ],
            "certifications": [
                "Oracle SQL",
                "Microsoft SQL Fundamentals"
            ],
            "projects": [
                "Employee Database",
                "Sales Dashboard"
            ]
        },

        "Power BI": {
            "courses": [
                "Power BI Basics",
                "DAX",
                "Dashboard Design"
            ],
            "certifications": [
                "Microsoft PL-300"
            ],
            "projects": [
                "Business Dashboard",
                "HR Analytics Dashboard"
            ]
        },

        "Web Dev": {
            "courses": [
                "HTML",
                "CSS",
                "JavaScript",
                "Flask",
                "REST API"
            ],
            "certifications": [
                "Meta Front-End",
                "FreeCodeCamp Responsive Web Design"
            ],
            "projects": [
                "Portfolio Website",
                "Career Recommendation Website"
            ]
        },

        "Networking": {
            "courses": [
                "Computer Networks",
                "Linux",
                "Cloud Basics"
            ],
            "certifications": [
                "Cisco CCNA",
                "CompTIA Network+"
            ],
            "projects": [
                "LAN Design",
                "Network Monitoring System"
            ]
        }

    }

    default_plan = {
        "courses": [
            f"{required_technical} Fundamentals",
            "Advanced Concepts",
            "Portfolio Development"
        ],
        "certifications": [
            f"{required_technical} Certification"
        ],
        "projects": [
            f"{target_career} Mini Project",
            "Capstone Project"
        ]
    }

    plan = roadmap_library.get(required_technical, default_plan)

    return jsonify({

        "career": target_career,

        "required_technical": required_technical,

        "required_soft": required_soft,

        "interest": interest,

        "readiness_score": 75,

        "courses": plan["courses"],

        "certifications": plan["certifications"],

        "projects": plan["projects"]

    })

@app.route('/saved-careers')
def saved_careers():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("saved_careers.html")

@app.route('/resume-analyzer')
def resume_analyzer():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("resume_analyzer.html")

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"})

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No selected file"})

    filename = secure_filename(file.filename)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(file_path)

    try:

        if filename.lower().endswith(".docx"):
            resume_text = extract_text_from_docx(file_path)

        elif filename.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_path)

        else:
            return jsonify({"error": "Only PDF and DOCX files are supported"})

        skill_keywords = [
            "python", "sql", "machine learning", "data analysis", "power bi",
            "flask", "html", "css", "javascript", "deep learning", "aws",
            "docker", "mlops", "statistics", "communication", "leadership",
            "problem solving"
        ]

        detected_skills = []

        for skill in skill_keywords:
            if skill in resume_text:
                detected_skills.append(skill.title())

        required_skills = [
            "Python",
            "SQL",
            "Machine Learning",
            "Power BI",
            "Statistics"
        ]

        missing_skills = []

        for skill in required_skills:
            if skill not in detected_skills:
                missing_skills.append(skill)

        skills_count = len(detected_skills)

        if skills_count >= 12:
            ats_score = 92
        elif skills_count >= 10:
            ats_score = 82
        elif skills_count >= 8:
            ats_score = 72
        elif skills_count >= 6:
            ats_score = 60
        elif skills_count >= 4:
            ats_score = 45
        else:
            ats_score = 35

        career_match = (
            90
            if "Python" in detected_skills or "Machine Learning" in detected_skills
            else 65
        )

        predicted_career = (
            "Data Scientist"
            if "Python" in detected_skills or "Machine Learning" in detected_skills
            else "Data Analyst"
        )

        if predicted_career == "Data Scientist":

            recommendation_text = (
                "Your resume strongly aligns with Data Science roles based on detected technical skills, "
                "programming experience and analytical keywords. Strengthening cloud technologies, "
                "advanced machine learning and real-world projects will further improve your profile."
            )

        elif predicted_career == "AI Engineer":

            recommendation_text = (
                "Your resume demonstrates a solid foundation for AI Engineering. "
                "Improving Deep Learning, Neural Networks, MLOps and model deployment "
                "skills will make your profile more competitive."
            )

        elif predicted_career == "Data Analyst":

            recommendation_text = (
                "Your resume aligns well with Data Analyst roles based on your analytical skills. "
                "Develop advanced SQL, Power BI, dashboard design and business intelligence expertise."
            )

        else:

            recommendation_text = (
                f"Your resume demonstrates good alignment with {predicted_career}. "
                "Continue improving technical skills, certifications and real-world projects."
            )

        return jsonify({

            "ats_score": ats_score,
            "skills_found": len(detected_skills),
            "missing_count": len(missing_skills),
            "career_match": career_match,
            "detected_skills": detected_skills,
            "missing_skills": missing_skills,

            "recommendations": [
                "Add measurable project outcomes.",
                "Include GitHub or portfolio links.",
                "Add relevant certifications.",
                "Improve keyword alignment with target career.",
                "Highlight technical and soft skills clearly."
            ],

            "predicted_career": predicted_career,
            "recommendation_text": recommendation_text

        })

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)
            

@app.route('/jobs')
def jobs():
    if "user" not in session:
        return redirect(url_for("login"))

    careers = sorted(df["Career Domain"].dropna().unique())

    return render_template("jobs.html", careers=careers)

@app.route("/recommend-jobs", methods=["POST"])
def recommend_jobs():
    data = request.get_json()
    target_career = data["target_career"]

    jobs_data = {
        "AI Engineer": [
            {
                "title": "AI Engineer",
                "company": "Google",
                "salary": "₹18–28 LPA",
                "location": "Bangalore",
                "match": 95,
                "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow"]
            },
            {
                "title": "Machine Learning Engineer",
                "company": "Amazon",
                "salary": "₹16–25 LPA",
                "location": "Hyderabad",
                "match": 91,
                "skills": ["Python", "ML", "AWS", "MLOps"]
            }
        ],

        "Data Analyst": [
            {
                "title": "Data Analyst",
                "company": "TCS",
                "salary": "₹6–10 LPA",
                "location": "Pune",
                "match": 92,
                "skills": ["SQL", "Excel", "Power BI", "Python"]
            },
            {
                "title": "Business Data Analyst",
                "company": "Infosys",
                "salary": "₹7–12 LPA",
                "location": "Bangalore",
                "match": 88,
                "skills": ["SQL", "Power BI", "Analytics", "Communication"]
            }
        ],

        "Backend Developer": [
            {
                "title": "Backend Developer",
                "company": "Microsoft",
                "salary": "₹14–22 LPA",
                "location": "Noida",
                "match": 94,
                "skills": ["Python", "Flask", "MySQL", "REST API"]
            },
            {
                "title": "Software Engineer",
                "company": "Wipro",
                "salary": "₹8–14 LPA",
                "location": "Chennai",
                "match": 87,
                "skills": ["Python", "SQL", "API", "Web Dev"]
            }
        ]
    }

    default_jobs = [
        {
            "title": target_career,
            "company": "Accenture",
            "salary": "₹6–12 LPA",
            "location": "Bangalore",
            "match": 85,
            "skills": ["Communication", "Problem Solving", "Domain Knowledge"]
        },
        {
            "title": "Associate " + target_career,
            "company": "Cognizant",
            "salary": "₹5–10 LPA",
            "location": "Hyderabad",
            "match": 80,
            "skills": ["Technical Skills", "Soft Skills", "Teamwork"]
        }
    ]

    jobs = jobs_data.get(target_career, default_jobs)

    return jsonify({"jobs": jobs})

@app.route('/saved-jobs')
def saved_jobs():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("saved_jobs.html")

@app.route('/ai-assistant')
def ai_assistant():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("ai_assistant.html")

@app.route("/ask-assistant", methods=["POST"])
def ask_assistant():
    data = request.get_json()

    question = data.get("question", "")
    predicted_career = data.get("predictedCareer", "Not available")
    resume_ats = data.get("resumeATS", "Not available")
    skill_match = data.get("skillMatch", "Not available")
    saved_jobs = data.get("savedJobs", 0)

    prompt = f"""
You are an AI Career Assistant for a Smart Career Guidance and Recommendation System.

User context:
- Predicted Career: {predicted_career}
- Resume ATS Score: {resume_ats}
- Skill Match Score: {skill_match}
- Saved Jobs Count: {saved_jobs}

Answer the user's question in a helpful, simple, student-friendly way.
Keep the answer career-focused.
Do not give very long answers.
Use clear steps if needed.

User question:
{question}
"""

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

    except Exception as e:
        print("Gemini Error:", e)

        answer = (
            "Sorry, I could not connect to the AI assistant right now. "
            "Please check your Gemini API key and internet connection."
        )

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)



