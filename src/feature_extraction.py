import json
import re
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"


FEATURE_COLUMNS = [
    "repetition_level",
    "rule_based_decision_level",
    "structured_data_level",
    "exception_rate",
    "process_stability",
    "manual_data_entry_level",
    "system_count",
    "handoff_count",
    "human_judgement_level",
    "compliance_risk_level",
    "customer_impact_level",
    "volume_level",
    "time_sensitivity",
    "data_quality_level",
]


def clamp(value, minimum=1, maximum=5):
    try:
        value = int(value)
    except Exception:
        value = 3

    return max(minimum, min(value, maximum))


def extract_json_from_response(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in LLM response.")

    return json.loads(match.group())


def keyword_fallback_extraction(description):
    text = description.lower()

    def count_keywords(keywords):
        return sum(1 for keyword in keywords if keyword in text)

    repetition = count_keywords([
        "daily", "weekly", "monthly", "repeated", "repetitive",
        "recurring", "routine", "frequent", "every day"
    ])

    rules = count_keywords([
        "if", "then", "rule", "condition", "criteria",
        "check", "validate", "approve", "reject"
    ])

    structured = count_keywords([
        "excel", "csv", "database", "form", "table",
        "sap", "salesforce", "crm", "erp"
    ])

    exceptions = count_keywords([
        "exception", "error", "missing", "mismatch",
        "incorrect", "manual review", "case by case", "escalation"
    ])

    judgement = count_keywords([
        "judgement", "interpret", "analyse", "investigate",
        "complex", "subjective", "review", "assess"
    ])

    compliance = count_keywords([
        "compliance", "legal", "privacy", "audit",
        "risk", "regulation", "financial", "health"
    ])

    systems = count_keywords([
        "sap", "salesforce", "servicenow", "jira", "excel",
        "outlook", "email", "crm", "erp", "database", "portal"
    ])

    handoffs = count_keywords([
        "send", "forward", "handoff", "transfer",
        "escalate", "approval", "manager", "team"
    ])

    manual_entry = count_keywords([
        "copy", "paste", "enter", "type", "manual",
        "download", "upload", "update", "fill"
    ])

    exception_rate = clamp(1 + exceptions)

    return {
        "repetition_level": clamp(1 + repetition),
        "rule_based_decision_level": clamp(1 + rules),
        "structured_data_level": clamp(1 + structured),
        "exception_rate": exception_rate,
        "process_stability": clamp(6 - exception_rate),
        "manual_data_entry_level": clamp(1 + manual_entry),
        "system_count": max(1, min(systems, 10)),
        "handoff_count": max(1, min(handoffs, 10)),
        "human_judgement_level": clamp(1 + judgement),
        "compliance_risk_level": clamp(1 + compliance),
        "customer_impact_level": 3,
        "volume_level": clamp(1 + repetition),
        "time_sensitivity": 3,
        "data_quality_level": 3,
    }


def extract_features_with_llm(description):
    prompt = f"""
You are an enterprise automation analyst.

Analyse the business process description and extract numerical features for an automation suitability ML model.

Return ONLY valid JSON.

Each value must be an integer.

Feature rules:
- Most features must be scored from 1 to 5.
- system_count must be from 1 to 10.
- handoff_count must be from 1 to 10.

Feature meaning:
1 = very low
2 = low
3 = medium
4 = high
5 = very high

Required JSON keys:
{FEATURE_COLUMNS}

Business process description:
{description}

Return JSON only.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()
    raw_response = result.get("response", "")

    extracted = extract_json_from_response(raw_response)

    cleaned = {}

    for column in FEATURE_COLUMNS:
        if column in ["system_count", "handoff_count"]:
            cleaned[column] = clamp(extracted.get(column, 3), 1, 10)
        else:
            cleaned[column] = clamp(extracted.get(column, 3), 1, 5)

    return cleaned


def extract_features_from_description(description):
    try:
        print("Using Ollama LLM extraction...")
        return extract_features_with_llm(description)

    except Exception as e:
        print("Ollama failed. Using keyword fallback.")
        print(e)

        return keyword_fallback_extraction(description)