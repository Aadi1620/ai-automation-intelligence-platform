def generate_final_decision(
    suitability_score,
    recommendation,
    complexity,
    business_value,
    recommendation_confidence,
    features
):
    suitability_score = float(suitability_score)

    high_judgement = features["human_judgement_level"] >= 4
    high_compliance = features["compliance_risk_level"] >= 4
    high_exceptions = features["exception_rate"] >= 4
    unstable_process = features["process_stability"] <= 2
    low_confidence = recommendation_confidence < 60

    if low_confidence:
        return {
            "decision": "Needs Further Review",
            "decision_level": "Medium",
            "summary": "The model confidence is not high enough to make a strong automation decision.",
            "action": "Review the extracted features manually and validate the process with a business analyst."
        }

    if recommendation == "Process Redesign" or unstable_process:
        return {
            "decision": "Redesign First",
            "decision_level": "High",
            "summary": "The process appears unstable or inefficient in its current form.",
            "action": "Standardise and redesign the process before investing in automation."
        }

    if recommendation == "Do Not Automate":
        return {
            "decision": "Do Not Automate Yet",
            "decision_level": "High",
            "summary": "The process is not currently suitable for automation.",
            "action": "Keep the process human-driven and reassess after simplification or standardisation."
        }

    if high_judgement or high_compliance or high_exceptions:
        return {
            "decision": "Automate Partially",
            "decision_level": "High",
            "summary": "The process contains automation potential, but some parts require human judgement, compliance review, or exception handling.",
            "action": "Automate repetitive and low-risk steps first while keeping sensitive decisions human-reviewed."
        }

    if recommendation == "AI Copilot":
        return {
            "decision": "Use AI Support Only",
            "decision_level": "Medium",
            "summary": "The process appears better suited to human decision support than full automation.",
            "action": "Build an AI copilot to assist users with research, drafting, classification, or decision support."
        }

    if suitability_score >= 75 and business_value == "High" and complexity in ["Low", "Medium"]:
        return {
            "decision": "Automate Now",
            "decision_level": "High",
            "summary": "The process has strong automation suitability, clear business value, and manageable implementation complexity.",
            "action": "Proceed with process mapping and a proof of concept automation build."
        }

    if suitability_score >= 50:
        return {
            "decision": "Automate Partially",
            "decision_level": "Medium",
            "summary": "The process has moderate automation potential but may need staged implementation.",
            "action": "Start with the most repetitive and rule-based parts of the process."
        }

    return {
        "decision": "Do Not Automate Yet",
        "decision_level": "Medium",
        "summary": "The process does not show enough automation readiness at this stage.",
        "action": "Review process maturity, data quality, and business value before proceeding."
    }