def calculate_operational_risk(features):
    risk = 0

    risk += features["exception_rate"] * 2
    risk += features["handoff_count"]
    risk += features["system_count"]

    risk -= features["process_stability"]

    return min(max(risk, 1), 10)


def calculate_compliance_risk(features):
    risk = 0

    risk += features["compliance_risk_level"] * 2
    risk += features["customer_impact_level"]

    if features["human_judgement_level"] >= 4:
        risk += 2

    return min(max(risk, 1), 10)


def calculate_automation_failure_risk(features):
    risk = 0

    risk += features["exception_rate"] * 2
    risk += features["human_judgement_level"]
    risk += features["system_count"]

    if features["process_stability"] <= 2:
        risk += 2

    return min(max(risk, 1), 10)


def calculate_data_risk(features):
    risk = 0

    risk += (6 - features["data_quality_level"]) * 2

    if features["structured_data_level"] <= 2:
        risk += 2

    return min(max(risk, 1), 10)


def calculate_process_maturity_risk(features):
    risk = 0

    risk += (6 - features["process_stability"]) * 2
    risk += features["exception_rate"]

    if features["handoff_count"] >= 5:
        risk += 2

    return min(max(risk, 1), 10)


def risk_label(score):
    if score <= 3:
        return "Low"

    if score <= 6:
        return "Medium"

    return "High"


def generate_risk_summary(features):
    operational_risk = calculate_operational_risk(features)

    compliance_risk = calculate_compliance_risk(features)

    automation_failure_risk = calculate_automation_failure_risk(features)

    data_risk = calculate_data_risk(features)

    process_maturity_risk = calculate_process_maturity_risk(features)

    return {
        "Operational Risk": {
            "score": operational_risk,
            "label": risk_label(operational_risk)
        },

        "Compliance Risk": {
            "score": compliance_risk,
            "label": risk_label(compliance_risk)
        },

        "Automation Failure Risk": {
            "score": automation_failure_risk,
            "label": risk_label(automation_failure_risk)
        },

        "Data Risk": {
            "score": data_risk,
            "label": risk_label(data_risk)
        },

        "Process Maturity Risk": {
            "score": process_maturity_risk,
            "label": risk_label(process_maturity_risk)
        }
    }