"""Professional PDF report generation for AegisX assessments."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak

from core.models import ScanResult


def build_pdf(result: ScanResult) -> bytes:
    """Return a readable, branded PDF executive assessment report."""

    buffer = BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="AegisTitle", parent=styles["Title"], textColor=colors.HexColor("#67e8f9"), alignment=TA_CENTER, fontSize=24, spaceAfter=8))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], textColor=colors.HexColor("#0f766e"), spaceBefore=12, spaceAfter=6))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm, topMargin=15 * mm, bottomMargin=15 * mm)
    story = [Paragraph("AEGISX", styles["AegisTitle"]), Paragraph("AI-Powered Cybersecurity Assessment Platform", styles["Normal"]), Spacer(1, 10)]
    score = result.score.score if result.score else 0.0
    level = result.score.risk_level if result.score else "Unknown"
    summary = [["Target", result.target.host], ["Scan ID", result.scan_id], ["Profile", result.profile.title()], ["Status", result.status], ["Risk score", f"{score:.2f} / 10.00 ({level})"], ["Completed", result.completed_at or "-"]]
    table = Table(summary, colWidths=[38 * mm, 130 * mm])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e6fffb")), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#99f6e4")), ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 6)]))
    story.extend([table, Spacer(1, 12), Paragraph("Executive Summary", styles["Section"]), Paragraph(f"AegisX completed a defensive assessment of <b>{result.target.host}</b>. The deterministic heuristic engine calculated a score of <b>{score:.2f}/10</b>, classified as <b>{level}</b>. Module failures, if any, are listed below rather than being hidden.", styles["BodyText"])] )
    story.append(Paragraph("Key Findings", styles["Section"]))
    finding_rows = [["Severity", "Category", "Finding", "Evidence"]]
    for finding in result.findings:
        finding_rows.append([finding.severity.title(), finding.category.title(), finding.title, finding.evidence or "-"])
    story.append(Table(finding_rows, repeatRows=1, colWidths=[22 * mm, 24 * mm, 72 * mm, 50 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.25, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 8), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 4)])))
    story.append(Paragraph("Network Exposure", styles["Section"]))
    port_rows = [["Port", "State", "Likely service", "Banner"]] + [[str(port.port), port.state, port.service, port.banner or "-"] for port in result.ports]
    story.append(Table(port_rows, repeatRows=1, colWidths=[18 * mm, 25 * mm, 50 * mm, 75 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#155e75")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.25, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 8), ("PADDING", (0, 0), (-1, -1), 4)])))
    if result.tls:
        story.append(Paragraph("TLS Inspection", styles["Section"]))
        tls = result.tls
        tls_rows = [["Handshake successful", str(tls.success)], ["TLS version", tls.tls_version or "-"], ["Cipher", tls.cipher or "-"], ["Subject", tls.subject or "-"], ["Issuer", tls.issuer or "-"], ["Days remaining", str(tls.days_remaining if tls.days_remaining is not None else "-")]]
        story.append(Table(tls_rows, colWidths=[45 * mm, 123 * mm], style=TableStyle([("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#ecfeff")), ("GRID", (0, 0), (-1, -1), 0.25, colors.grey), ("PADDING", (0, 0), (-1, -1), 5)])))
    story.append(Paragraph("Recommendations", styles["Section"]))
    for finding in result.findings:
        if finding.severity.lower() != "info":
            story.append(Paragraph(f"<b>{finding.title}</b> — {finding.remediation}", styles["Small"]))
            story.append(Spacer(1, 3))
    if result.module_errors:
        story.append(Paragraph("Module Warnings", styles["Section"]))
        story.append(Paragraph("; ".join(f"{name}: {error}" for name, error in result.module_errors.items()), styles["Small"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Authorized-use notice: Only scan systems, domains, and infrastructure you own or are explicitly authorized to assess. AegisX performs defensive, non-exploitative checks and does not guarantee the absence of vulnerabilities.", styles["Small"]))
    doc.build(story)
    return buffer.getvalue()


def write_pdf(result: ScanResult, path: str | Path) -> str:
    """Write a PDF report and return its path."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(build_pdf(result))
    return str(destination)
