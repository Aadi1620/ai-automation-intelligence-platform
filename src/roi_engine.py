def calculate_total_initial_investment(
    software_cost,
    hardware_cost,
    implementation_cost,
    integration_cost,
    training_cost,
):
    return (
        software_cost
        + hardware_cost
        + implementation_cost
        + integration_cost
        + training_cost
    )


def calculate_direct_labour_savings(
    transactions_per_month,
    avg_handling_time_minutes,
    automation_reduction_percent,
    hourly_cost,
):
    monthly_hours = (transactions_per_month * avg_handling_time_minutes) / 60

    annual_hours = monthly_hours * 12

    hours_saved = annual_hours * (automation_reduction_percent / 100)

    direct_savings = hours_saved * hourly_cost

    return hours_saved, direct_savings


def calculate_indirect_savings(
    error_correction_hours_per_month,
    manager_review_hours_per_month,
    hourly_cost,
    error_reduction_percent,
    review_reduction_percent,
):
    annual_error_hours = error_correction_hours_per_month * 12
    annual_review_hours = manager_review_hours_per_month * 12

    saved_error_hours = annual_error_hours * (error_reduction_percent / 100)
    saved_review_hours = annual_review_hours * (review_reduction_percent / 100)

    indirect_savings = (saved_error_hours + saved_review_hours) * hourly_cost

    return saved_error_hours + saved_review_hours, indirect_savings


def calculate_roi(
    net_annual_savings,
    total_initial_investment,
):
    if total_initial_investment <= 0:
        return 0

    return (net_annual_savings / total_initial_investment) * 100


def calculate_payback_period(
    total_initial_investment,
    net_annual_savings,
):
    if net_annual_savings <= 0:
        return None

    monthly_savings = net_annual_savings / 12

    return total_initial_investment / monthly_savings


def generate_roi_estimate_v2(
    software_cost,
    hardware_cost,
    implementation_cost,
    integration_cost,
    training_cost,
    annual_maintenance_cost,
    transactions_per_month,
    avg_handling_time_minutes,
    automation_reduction_percent,
    hourly_cost,
    error_correction_hours_per_month,
    manager_review_hours_per_month,
    error_reduction_percent,
    review_reduction_percent,
):
    total_initial_investment = calculate_total_initial_investment(
        software_cost,
        hardware_cost,
        implementation_cost,
        integration_cost,
        training_cost,
    )

    hours_saved_per_year, direct_labour_savings = calculate_direct_labour_savings(
        transactions_per_month,
        avg_handling_time_minutes,
        automation_reduction_percent,
        hourly_cost,
    )

    indirect_hours_saved, indirect_savings = calculate_indirect_savings(
        error_correction_hours_per_month,
        manager_review_hours_per_month,
        hourly_cost,
        error_reduction_percent,
        review_reduction_percent,
    )

    gross_annual_savings = direct_labour_savings + indirect_savings

    net_annual_savings = gross_annual_savings - annual_maintenance_cost

    roi_percent = calculate_roi(
        net_annual_savings,
        total_initial_investment,
    )

    payback_period_months = calculate_payback_period(
        total_initial_investment,
        net_annual_savings,
    )

    return {
        "total_initial_investment": round(total_initial_investment, 2),
        "hours_saved_per_year": round(hours_saved_per_year, 1),
        "indirect_hours_saved_per_year": round(indirect_hours_saved, 1),
        "direct_labour_savings": round(direct_labour_savings, 2),
        "indirect_savings": round(indirect_savings, 2),
        "gross_annual_savings": round(gross_annual_savings, 2),
        "annual_maintenance_cost": round(annual_maintenance_cost, 2),
        "net_annual_savings": round(net_annual_savings, 2),
        "roi_percent": round(roi_percent, 1),
        "payback_period_months": None if payback_period_months is None else round(payback_period_months, 1),
    }