def explain_score(features, suitability_score):
    reasons = []

    if features["repetition_level"] >= 4:
        reasons.append("High repetition increases automation suitability.")

    if features["rule_based_decision_level"] >= 4:
        reasons.append("The process has strong rule-based decision patterns.")

    if features["structured_data_level"] >= 4:
        reasons.append("Structured data makes the process easier to automate.")

    if features["manual_data_entry_level"] >= 4:
        reasons.append("High manual data entry creates strong automation potential.")

    if features["exception_rate"] >= 4:
        reasons.append("High exception rate reduces automation suitability.")

    if features["human_judgement_level"] >= 4:
        reasons.append("High human judgement requirement limits full automation.")

    if features["compliance_risk_level"] >= 4:
        reasons.append("Compliance risk means human oversight is required.")

    if features["process_stability"] <= 2:
        reasons.append("Low process stability suggests redesign may be needed before automation.")

    if not reasons:
        reasons.append("The recommendation is based on the overall balance of process features.")

    if suitability_score >= 75:
        score_summary = "This process is a strong automation candidate."
    elif suitability_score >= 50:
        score_summary = "This process has moderate automation potential."
    else:
        score_summary = "This process is not currently a strong automation candidate."

    return score_summary, reasons


def explain_recommendation(recommendation, features):
    if recommendation == "RPA":
        return (
            "RPA is suitable because the process appears repetitive, rule-based, and system-driven."
        )

    if recommendation == "Workflow Automation":
        return (
            "Workflow automation is suitable because the process likely involves structured handoffs, approvals, and system-triggered actions."
        )

    if recommendation == "AI Copilot":
        return (
            "An AI copilot is suitable because the process appears to require human judgement, interpretation, or decision support."
        )

    if recommendation == "AI Agent":
        return (
            "An AI agent may be suitable because the process involves multi-step reasoning or dynamic task execution."
        )

    if recommendation == "Intelligent Document Processing":
        return (
            "Intelligent Document Processing is suitable because the process likely involves document extraction, validation, or semi-structured data."
        )

    if recommendation == "Process Redesign":
        return (
            "Process redesign is recommended because the process appears unstable, complex, exception-heavy, or inefficient in its current form."
        )

    if recommendation == "Human-Assisted Automation":
        return (
            "Human-assisted automation is suitable because parts of the process can be automated, but judgement or compliance review should remain with people."
        )

    if recommendation == "Do Not Automate":
        return (
            "Full automation is not recommended because the process may be too judgement-heavy, unstable, low-volume, or risky."
        )

    return "The recommendation is based on the predicted process characteristics."


def identify_risks(features):
    risks = []

    if features["exception_rate"] >= 4:
        risks.append("High exception rate may increase automation failure or manual fallback.")

    if features["human_judgement_level"] >= 4:
        risks.append("High judgement requirement may reduce automation reliability.")

    if features["compliance_risk_level"] >= 4:
        risks.append("Compliance-sensitive steps require governance and audit controls.")

    if features["data_quality_level"] <= 2:
        risks.append("Poor data quality may reduce model and automation performance.")

    if features["system_count"] >= 5:
        risks.append("Multiple systems increase integration complexity.")

    if features["handoff_count"] >= 5:
        risks.append("Frequent handoffs may indicate process fragmentation.")

    if not risks:
        risks.append("No major risks were detected from the extracted features.")

    return risks


def identify_human_review_areas(features):
    review_areas = []

    if features["human_judgement_level"] >= 3:
        review_areas.append("Decision-making steps should remain human-reviewed.")

    if features["compliance_risk_level"] >= 3:
        review_areas.append("Compliance-sensitive steps should require approval or audit trails.")

    if features["exception_rate"] >= 3:
        review_areas.append("Exception cases should be routed to human users.")

    if features["customer_impact_level"] >= 4:
        review_areas.append("Customer-impacting outcomes should include human escalation paths.")

    if not review_areas:
        review_areas.append("Most steps appear suitable for automation with standard monitoring.")

    return review_areas


def suggest_next_action(recommendation, suitability_score, features):
    if suitability_score >= 75 and recommendation in [
        "RPA",
        "Workflow Automation",
        "Intelligent Document Processing",
    ]:
        return "Proceed to detailed process mapping and automation proof of concept."

    if recommendation == "Process Redesign":
        return "Redesign and stabilise the process before investing in automation."

    if recommendation == "AI Copilot":
        return "Build a decision-support prototype instead of full automation."

    if recommendation == "Human-Assisted Automation":
        return "Automate low-risk steps first and keep judgement-heavy steps human-driven."

    if recommendation == "Do Not Automate":
        return "Do not automate this process yet. Review whether the process should be simplified or standardised first."

    return "Conduct stakeholder review before deciding the automation roadmap."


def generate_explanation(features, suitability_score, recommendation):
    score_summary, score_reasons = explain_score(features, suitability_score)
    recommendation_reason = explain_recommendation(recommendation, features)
    risks = identify_risks(features)
    human_review_areas = identify_human_review_areas(features)
    next_action = suggest_next_action(recommendation, suitability_score, features)

    return {
        "score_summary": score_summary,
        "score_reasons": score_reasons,
        "recommendation_reason": recommendation_reason,
        "risks": risks,
        "human_review_areas": human_review_areas,
        "next_action": next_action,
    }