from flask import Flask, jsonify, render_template, request
from routes.dashboard import calculate_gpa, classify_gpa

app = Flask(__name__)


@app.get("/")
def dashboard():
    return render_template("index.html")


@app.post("/dashboard/gpa")
def calculate_dashboard_gpa():
    payload = request.get_json(silent=True)
    courses = payload.get("courses") if isinstance(payload, dict) else None

    if not isinstance(courses, list):
        return jsonify({"error": "Request must include a courses list"}), 400

    try:
        gpa = calculate_gpa(courses)
        classification = classify_gpa(gpa)
    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({"gpa": gpa, "classification": classification})
