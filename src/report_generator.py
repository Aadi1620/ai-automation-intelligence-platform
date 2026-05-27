from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def add_section(story, title, styles):
    story.append(Spacer(1, 12))
    story.append(Paragraph(title, styles["Heading2"]))
    story.append(Spacer(1, 6))


def add_bullets(story, items, styles):
    for item in items:
        story.append(Paragraph(f"- {item}", styles["BodyText"]))


def generate_report(
    process_description,
    suitability_score,
    recommendation,
    complexity,
    business_value,
    recommendation_confidence,
    complexity_confidence,
    business_value_confidence,
    final_decision,
    readiness_assessment,
    roi_estimate,
    risk_summary,
    explanation,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    report_date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    story.append(Paragraph("Automation Assessment Report", styles["Title"]))
    story.append(Paragraph(f"Generated on: {report_date}", styles["Normal"]))
    story.append(Spacer(1, 16))

    add_section(story, "1. Process Description", styles)
    story.append(Paragraph(process_description, styles["BodyText"]))

    add_section(story, "2. Automation Prediction Summary", styles)

    prediction_table = Table([
        ["Metric", "Value"],
        ["Automation Suitability Score", f"{round(suitability_score, 1)}/100"],
        ["Recommended Automation Type", recommendation],
        ["Implementation Complexity", complexity],
        ["Business Value Potential", business_value],
        ["Recommendation Confidence", f"{round(recommendation_confidence, 1)}%"],
        ["Complexity Confidence", f"{round(complexity_confidence, 1)}%"],
        ["Business Value Confidence", f"{round(business_value_confidence, 1)}%"],
    ])

    prediction_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    story.append(prediction_table)

    add_section(story, "3. Final Business Decision", styles)
    story.append(Paragraph(f"Decision: {final_decision['decision']}", styles["BodyText"]))
    story.append(Paragraph(f"Confidence Level: {final_decision['decision_level']}", styles["BodyText"]))
    story.append(Paragraph(final_decision["summary"], styles["BodyText"]))
    story.append(Paragraph(f"Recommended Action: {final_decision['action']}", styles["BodyText"]))

    add_section(story, "4. Enterprise Automation Readiness", styles)
    story.append(Paragraph(f"Readiness Score: {readiness_assessment['score']}%", styles["BodyText"]))
    story.append(Paragraph(f"Readiness Level: {readiness_assessment['level']}", styles["BodyText"]))

    story.append(Paragraph("Strengths:", styles["Heading3"]))
    add_bullets(story, readiness_assessment["strengths"], styles)

    story.append(Paragraph("Weaknesses:", styles["Heading3"]))
    add_bullets(story, readiness_assessment["weaknesses"], styles)

    story.append(Paragraph(
        f"Recommended Readiness Action: {readiness_assessment['recommended_action']}",
        styles["BodyText"]
    ))

    add_section(story, "5. ROI Estimate", styles)

    roi_table = Table([
        ["Metric", "Value"],
        ["Total Initial Investment", f"${roi_estimate['total_initial_investment']:,.2f}"],
        ["Hours Saved Per Year", f"{roi_estimate['hours_saved_per_year']} hrs"],
        ["Direct Labour Savings", f"${roi_estimate['direct_labour_savings']:,.2f}"],
        ["Indirect Savings", f"${roi_estimate['indirect_savings']:,.2f}"],
        ["Gross Annual Savings", f"${roi_estimate['gross_annual_savings']:,.2f}"],
        ["Annual Maintenance Cost", f"${roi_estimate['annual_maintenance_cost']:,.2f}"],
        ["Net Annual Savings", f"${roi_estimate['net_annual_savings']:,.2f}"],
        ["Payback Period", f"{roi_estimate['payback_period_months']} months"],
        ["Projected ROI", f"{roi_estimate['roi_percent']}%"],
    ])

    roi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    story.append(roi_table)

    add_section(story, "6. Enterprise Risk Assessment", styles)

    risk_table_data = [["Risk Type", "Risk Level", "Score"]]

    for risk_name, risk_data in risk_summary.items():
        risk_table_data.append([
            risk_name,
            risk_data["label"],
            f"{risk_data['score']}/10",
        ])

    risk_table = Table(risk_table_data)

    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    story.append(risk_table)

    add_section(story, "7. Explanation", styles)
    story.append(Paragraph(explanation["score_summary"], styles["BodyText"]))

    story.append(Paragraph("Key Reasons:", styles["Heading3"]))
    add_bullets(story, explanation["score_reasons"], styles)

    story.append(Paragraph("Recommendation Reason:", styles["Heading3"]))
    story.append(Paragraph(explanation["recommendation_reason"], styles["BodyText"]))

    story.append(Paragraph("Risks:", styles["Heading3"]))
    add_bullets(story, explanation["risks"], styles)

    story.append(Paragraph("Human Review Areas:", styles["Heading3"]))
    add_bullets(story, explanation["human_review_areas"], styles)

    story.append(Paragraph("Suggested Next Action:", styles["Heading3"]))
    story.append(Paragraph(explanation["next_action"], styles["BodyText"]))

    add_section(story, "8. Disclaimer", styles)
    story.append(Paragraph(
        "This report is generated using a prototype AI and ML-based automation assessment system. "
        "Results should be validated with real operational data, stakeholder review, process mapping, "
        "and financial analysis before business implementation.",
        styles["BodyText"]
    ))

    doc.build(story)

    buffer.seek(0)

    return buffer