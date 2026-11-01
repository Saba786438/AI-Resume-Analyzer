
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from docx import Document
from pathlib import Path
from werkzeug.utils import secure_filename
import re
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def extract_text(filepath):
    if filepath.lower().endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    document = Document(filepath)
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs
    )


SKILLS = [
    "python", "java", "javascript", "html", "css",
    "flask", "django", "sql", "mysql", "mongodb",
    "react", "node.js", "machine learning",
    "data analysis", "git", "excel", "communication",
    "problem solving", "rest api", "aws"
]


def analyze_resume(text, job_description=""):
    resume_lower = text.lower()
    job_lower = job_description.lower()

    found_skills = [
        skill for skill in SKILLS
        if re.search(
            r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
            resume_lower
        )
    ]

    job_skills = [
        skill for skill in SKILLS
        if re.search(
            r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
            job_lower
        )
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in found_skills
    ]

    if job_skills:
        matched = len(
            set(found_skills) & set(job_skills)
        )
        match_score = round(
            matched / len(set(job_skills)) * 100
        )
    else:
        match_score = 0

    score = 0
    if len(text.split()) >= 100:
        score += 25
    if any(word in resume_lower for word in
           ["education", "qualification"]):
        score += 15
    if any(word in resume_lower for word in
           ["experience", "internship"]):
        score += 20
    if any(word in resume_lower for word in
           ["project", "projects"]):
        score += 15
    if found_skills:
        score += 15
    if any(word in resume_lower for word in
           ["email", "phone", "contact"]):
        score += 10

    suggestions = []

    if "experience" not in resume_lower:
        suggestions.append(
            "Add relevant work experience or internships."
        )
    if "projects" not in resume_lower and "project" not in resume_lower:
        suggestions.append(
            "Include projects that demonstrate your skills."
        )
    if not found_skills:
        suggestions.append(
            "Add a clearly labelled skills section."
        )
    if missing_skills:
        suggestions.append(
            "Review the missing job skills and learn or "
            "highlight relevant ones you genuinely possess."
        )
    if not suggestions:
        suggestions.append(
            "Review formatting and quantify your achievements."
        )

    return {
        "score": score,
        "skills": found_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
        "suggestions": suggestions
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("resume")
        job_description = request.form.get(
            "job_description", ""
        )

        if not file or not file.filename:
            return render_template(
                "index.html", error="Please select a resume."
            )

        if not allowed_file(file.filename):
            return render_template(
                "index.html",
                error="Please upload a PDF or DOCX file."
            )

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        file.save(filepath)

        try:
            text = extract_text(filepath)
            if not text.strip():
                return render_template(
                    "index.html",
                    error="No readable text found. "
                    "Scanned PDFs may need OCR."
                )

            results = analyze_resume(
                text, job_description
            )

            return render_template(
                "dashboard.html",
                results=results
            )
        except Exception:
            return render_template(
                "index.html",
                error="Could not read this file. "
                "Please try another PDF or DOCX."
            )
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
