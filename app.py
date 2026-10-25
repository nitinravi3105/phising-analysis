from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
from analyzer import analyze_message
from database import init_db, save_evidence, list_evidence, get_evidence
from evidence_report import create_pdf_report
from pathlib import Path
import io
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-for-production")
BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

with app.app_context():
    init_db()

@app.route("/")
def index():
    recent = list_evidence(limit=5)
    stats = list_evidence(limit=None)
    return render_template("index.html", recent=recent, total=len(stats),
                           high=sum(1 for x in stats if x["risk_level"] == "High"),
                           medium=sum(1 for x in stats if x["risk_level"] == "Medium"))

@app.route("/analyze", methods=["POST"])
def analyze():
    message = request.form.get("message", "").strip()
    message_type = request.form.get("message_type", "Message").strip()
    if not message:
        flash("Please enter a message or URL to analyze.", "error")
        return redirect(url_for("index"))
    if len(message) > 10000:
        flash("Input is too long. Please use 10,000 characters or fewer.", "error")
        return redirect(url_for("index"))
    if message_type not in {"SMS", "Email", "URL", "Message"}:
        message_type = "Message"

    result = analyze_message(message, message_type)
    evidence_id = save_evidence(
        content=message,
        message_type=message_type,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        indicators=result["indicators"],
        summary=result["summary"],
        content_hash=result["content_hash"],
    )
    record = get_evidence(evidence_id)
    return render_template("result.html", record=record, indicators=result["indicators"])

@app.route("/history")
def history():
    records = list_evidence(limit=200)
    return render_template("history.html", records=records)

@app.route("/evidence/<int:evidence_id>")
def evidence_detail(evidence_id):
    record = get_evidence(evidence_id)
    if not record:
        abort(404)
    return render_template("result.html", record=record, indicators=record["indicators_list"])

@app.route("/report/<int:evidence_id>.pdf")
def download_report(evidence_id):
    record = get_evidence(evidence_id)
    if not record:
        abort(404)
    pdf_bytes = create_pdf_report(record)
    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf",
                     as_attachment=True, download_name=f"evidence_{evidence_id}.pdf")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)




