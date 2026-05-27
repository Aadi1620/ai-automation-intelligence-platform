def calculate_readiness_score(readiness_inputs):
    total_score = sum(readiness_inputs.values())

    max_score = len(readiness_inputs) * 5

    percentage_score = (total_score / max_score) * 100

    return round(percentage_score, 1)
#test comment

def determine_readiness_level(score):
    if score < 20:
        return "Level 1 – Not Ready"

    if score < 40:
        return "Level 2 – Early Readiness"

    if score < 60:
        return "Level 3 – Moderately Ready"

    if score < 80:
        return "Level 4 – Operationally Ready"

    return "Level 5 – Enterprise Automation Ready"


def identify_readiness_strengths(readiness_inputs):
    strengths = []

    for key, value in readiness_inputs.items():

        if value >= 4:
            strengths.append(format_label(key))

    if not strengths:
        strengths.append("No major readiness strengths detected.")

    return strengths


def identify_readiness_weaknesses(readiness_inputs):
    weaknesses = []

    for key, value in readiness_inputs.items():

        if value <= 2:
            weaknesses.append(format_label(key))

    if not weaknesses:
        weaknesses.append("No major readiness weaknesses detected.")

    return weaknesses


def format_label(text):
    return text.replace("_", " ").title()


def generate_readiness_action(level):
    if level == "Level 1 – Not Ready":
        return (
            "Focus on documenting and stabilising the process before pursuing automation."
        )

    if level == "Level 2 – Early Readiness":
        return (
            "Improve governance, ownership, and operational consistency before scaling automation."
        )

    if level == "Level 3 – Moderately Ready":
        return (
            "The organisation is suitable for limited or pilot automation initiatives."
        )

    if level == "Level 4 – Operationally Ready":
        return (
            "Proceed with automation implementation and operational governance planning."
        )

    return (
        "The organisation appears mature enough for enterprise-scale intelligent automation initiatives."
    )


def generate_automation_readiness_assessment(readiness_inputs):
    score = calculate_readiness_score(readiness_inputs)

    level = determine_readiness_level(score)

    strengths = identify_readiness_strengths(readiness_inputs)

    weaknesses = identify_readiness_weaknesses(readiness_inputs)

    action = generate_readiness_action(level)

    return {
        "score": score,
        "level": level,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommended_action": action,
    }