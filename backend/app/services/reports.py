from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime


def create_scan_report(scan, output_dir: str = "uploads/reports") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    report_path = Path(output_dir) / f"scan_report_{scan.id}.pdf"
    c = canvas.Canvas(str(report_path), pagesize=letter)
    width, height = letter
    y = height - inch
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, y, "DeepGuard Scan Report")
    y -= 0.4 * inch
    c.setFont("Helvetica", 11)
    rows = [
        ("Scan ID", str(scan.id)),
        ("Original File", scan.original_filename),
        ("Modality", scan.modality),
        ("Prediction", scan.prediction),
        ("Confidence", f"{scan.confidence:.2f}%"),
        ("File Type", scan.file_type),
        ("File Size", f"{scan.file_size} bytes"),
        ("Created At", scan.created_at.strftime("%Y-%m-%d %H:%M:%S") if scan.created_at else datetime.utcnow().isoformat()),
    ]
    for key, value in rows:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(inch, y, f"{key}:")
        c.setFont("Helvetica", 11)
        c.drawString(2.4 * inch, y, value[:80])
        y -= 0.28 * inch
    y -= 0.2 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, y, "Explanation")
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)
    text = c.beginText(inch, y)
    for line in (scan.explanation or "No explanation available.").splitlines():
        text.textLine(line[:95])
    c.drawText(text)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(inch, 0.7 * inch, "Note: Starter build uses mock AI results. Replace detector.py with trained model inference for final defense.")
    c.save()
    return str(report_path).replace("\\", "/")
