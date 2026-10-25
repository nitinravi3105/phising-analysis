from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from xml.sax.saxutils import escape

def create_pdf_report(record):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=16*mm, bottomMargin=16*mm)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Phishing Message Analysis — Digital Evidence Report", styles["Title"]),
        Spacer(1, 8),
        Paragraph("<b>Educational demonstration report</b> — automated indicators are not proof of phishing.", styles["BodyText"]),
        Spacer(1, 10),
    ]
    rows = [
        ["Evidence ID", str(record["id"])],
        ["Recorded (UTC)", escape(record["created_at"])],
        ["Input type", escape(record["message_type"])],
        ["Risk score", f'{record["risk_score"]}/100'],
        ["Risk level", escape(record["risk_level"])],
        ["SHA-256 content hash", escape(record["content_hash"])],
    ]
    table = Table(rows, colWidths=[42*mm, 125*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#e8eef7")),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.extend([table, Spacer(1, 12), Paragraph("Submitted content", styles["Heading2"]),
                  Paragraph(escape(record["content"]).replace("\n", "<br/>"), styles["BodyText"]),
                  Spacer(1, 12), Paragraph("Analysis summary", styles["Heading2"]),
                  Paragraph(escape(record["summary"]), styles["BodyText"]),
                  Spacer(1, 8), Paragraph("Indicators", styles["Heading2"])])
    indicators = record.get("indicators_list", record.get("indicators", []))
    for item in indicators:
        story.append(Paragraph(f"<b>{escape(item['name'])}</b> ({item['points']} points): {escape(item['detail'])}", styles["BodyText"]))
        story.append(Spacer(1, 5))
    story.extend([Spacer(1, 12), Paragraph("Limitations and handling notes", styles["Heading2"]),
                  Paragraph("This report records the submitted text and the output of a simple rule-based demonstration. It does not verify sender identity, perform live threat intelligence checks, establish a legally validated chain of custody, or prove that a message is malicious. Preserve original files and metadata separately when conducting a real investigation.", styles["BodyText"])])
    doc.build(story)
    return buffer.getvalue()
