import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
MODEL_DIR = BASE_DIR / "models"

sys.path.append(str(SRC_DIR))

from feature_extraction import extract_features_from_description
from explanation_engine import generate_explanation
from decision_engine import generate_final_decision
from risk_engine import generate_risk_summary
from shap_explainer import generate_shap_explanation
from roi_engine import generate_roi_estimate_v2
from automation_readiness_engine import generate_automation_readiness_assessment
from report_generator import generate_report


score_model = joblib.load(MODEL_DIR / "score_model.pkl")
recommendation_model = joblib.load(MODEL_DIR / "recommendation_model.pkl")
complexity_model = joblib.load(MODEL_DIR / "complexity_model.pkl")
business_value_model = joblib.load(MODEL_DIR / "business_value_model.pkl")


st.set_page_config(
    page_title="Automation Intelligence Platform",
    layout="wide"
)

st.title("AI Automation Intelligence Platform")

st.markdown(
    "Enterprise automation assessment platform for suitability prediction, ROI, readiness, risk, and explainability."
)

tabs = st.tabs([
    "Process Input",
    "Prediction Results",
    "ROI & Readiness",
    "Risk & Explainability",
    "Report Export"
])


with st.sidebar:

    st.header("Process Input")

    process_description = st.text_area(
        "Business Process Description",
        height=220,
        placeholder="Describe the process here..."
    )

    st.markdown("---")
    st.header("ROI Assumptions")

    transactions_per_month = st.number_input(
        "Transactions per month",
        min_value=1,
        value=1000,
        step=100
    )

    avg_handling_time_minutes = st.number_input(
        "Average handling time per transaction in minutes",
        min_value=1.0,
        value=8.0,
        step=1.0
    )

    hourly_cost = st.number_input(
        "Fully loaded hourly wage including benefits",
        min_value=10.0,
        max_value=300.0,
        value=45.0,
        step=5.0
    )

    automation_reduction_percent = st.slider(
        "Expected automation reduction in manual work %",
        0,
        100,
        60
    )

    error_correction_hours_per_month = st.number_input(
        "Error correction hours per month",
        min_value=0.0,
        value=20.0,
        step=5.0
    )

    manager_review_hours_per_month = st.number_input(
        "Management review hours per month",
        min_value=0.0,
        value=15.0,
        step=5.0
    )

    error_reduction_percent = st.slider(
        "Expected error reduction %",
        0,
        100,
        40
    )

    review_reduction_percent = st.slider(
        "Expected management review reduction %",
        0,
        100,
        30
    )

    st.markdown("---")
    st.header("Investment Assumptions")

    software_cost = st.number_input(
        "Software / licence cost",
        min_value=0.0,
        value=5000.0,
        step=1000.0
    )

    hardware_cost = st.number_input(
        "Hardware cost",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )

    implementation_cost = st.number_input(
        "Implementation cost",
        min_value=0.0,
        value=12000.0,
        step=1000.0
    )

    integration_cost = st.number_input(
        "Integration cost",
        min_value=0.0,
        value=5000.0,
        step=1000.0
    )

    training_cost = st.number_input(
        "Staff training cost",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )

    annual_maintenance_cost = st.number_input(
        "Annual maintenance cost",
        min_value=0.0,
        value=4000.0,
        step=500.0
    )

    st.markdown("---")
    st.header("Automation Readiness")

    process_documentation_quality = st.slider(
        "Process Documentation Quality",
        1,
        5,
        3
    )

    process_owner_clarity = st.slider(
        "Process Ownership Clarity",
        1,
        5,
        3
    )

    sla_defined = st.slider(
        "SLA / KPI Definition Maturity",
        1,
        5,
        3
    )

    exception_management_maturity = st.slider(
        "Exception Management Maturity",
        1,
        5,
        3
    )

    governance_readiness = st.slider(
        "Governance & Compliance Readiness",
        1,
        5,
        3
    )

    stakeholder_alignment = st.slider(
        "Stakeholder Alignment",
        1,
        5,
        3
    )

    operational_stability = st.slider(
        "Operational Stability",
        1,
        5,
        3
    )

    automation_support_readiness = st.slider(
        "Automation Support Readiness",
        1,
        5,
        3
    )

    change_stability = st.slider(
        "Process Change Stability",
        1,
        5,
        3
    )

    monitoring_maturity = st.slider(
        "Monitoring & Reporting Maturity",
        1,
        5,
        3
    )

    analyse_clicked = st.button(
        "Analyse Process",
        use_container_width=True
    )


if analyse_clicked:

    if not process_description.strip():
        st.error("Please enter a process description first.")

    else:
        extracted_features = extract_features_from_description(process_description)

        readiness_inputs = {
            "process_documentation_quality": process_documentation_quality,
            "process_owner_clarity": process_owner_clarity,
            "sla_defined": sla_defined,
            "exception_management_maturity": exception_management_maturity,
            "governance_readiness": governance_readiness,
            "stakeholder_alignment": stakeholder_alignment,
            "operational_stability": operational_stability,
            "automation_support_readiness": automation_support_readiness,
            "change_stability": change_stability,
            "monitoring_maturity": monitoring_maturity,
        }

        readiness_assessment = generate_automation_readiness_assessment(
            readiness_inputs
        )

        input_data = pd.DataFrame([extracted_features])

        suitability_score = score_model.predict(input_data)[0]
        recommendation = recommendation_model.predict(input_data)[0]
        complexity = complexity_model.predict(input_data)[0]
        business_value = business_value_model.predict(input_data)[0]

        recommendation_probabilities = recommendation_model.predict_proba(input_data)[0]
        complexity_probabilities = complexity_model.predict_proba(input_data)[0]
        business_value_probabilities = business_value_model.predict_proba(input_data)[0]

        recommendation_confidence = recommendation_probabilities.max() * 100
        complexity_confidence = complexity_probabilities.max() * 100
        business_value_confidence = business_value_probabilities.max() * 100

        explanation = generate_explanation(
            extracted_features,
            suitability_score,
            recommendation
        )

        final_decision = generate_final_decision(
            suitability_score,
            recommendation,
            complexity,
            business_value,
            recommendation_confidence,
            extracted_features
        )

        risk_summary = generate_risk_summary(extracted_features)

        shap_explanation = generate_shap_explanation(
            score_model,
            input_data
        )

        roi_estimate = generate_roi_estimate_v2(
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
        )

        assessment_report = generate_report(
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
        )

        with tabs[0]:
            st.subheader("Process Description")
            st.write(process_description)

            st.divider()

            st.subheader("Extracted Process Features")
            st.dataframe(input_data, use_container_width=True)

        with tabs[1]:
            st.subheader("Executive Summary")

            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

            with summary_col1:
                st.metric(
                    "Automation Score",
                    f"{round(suitability_score, 1)}/100"
                )

            with summary_col2:
                st.metric(
                    "Automation Type",
                    recommendation
                )

            with summary_col3:
                st.metric(
                    "Projected ROI",
                    f"{roi_estimate['roi_percent']}%"
                )

            with summary_col4:
                st.metric(
                    "Business Decision",
                    final_decision["decision"]
                )

            st.divider()

            decision = final_decision["decision"]

            if decision == "Automate Now":
                st.success("Recommended for Immediate Automation")
            elif decision == "Automate Partially":
                st.warning("Recommended for Partial Automation")
            elif decision == "Use AI Support Only":
                st.info("Recommended for AI-Assisted Support")
            else:
                st.error("Not Currently Recommended for Full Automation")

            st.subheader("Prediction Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Automation Suitability Score",
                    f"{round(suitability_score, 1)}/100"
                )

                st.metric(
                    "Recommended Automation Type",
                    recommendation
                )

                st.caption(f"Confidence: {round(recommendation_confidence, 1)}%")

            with col2:
                st.metric(
                    "Implementation Complexity",
                    complexity
                )

                st.caption(f"Confidence: {round(complexity_confidence, 1)}%")

                st.metric(
                    "Business Value Potential",
                    business_value
                )

                st.caption(f"Confidence: {round(business_value_confidence, 1)}%")

            st.divider()

            st.subheader("Final Business Decision")

            decision_level = final_decision["decision_level"]

            if decision in ["Automate Now"]:
                st.success(f"{decision} | Confidence Level: {decision_level}")
            elif decision in ["Automate Partially", "Use AI Support Only", "Needs Further Review"]:
                st.warning(f"{decision} | Confidence Level: {decision_level}")
            else:
                st.error(f"{decision} | Confidence Level: {decision_level}")

            st.write(final_decision["summary"])

            st.markdown("#### Recommended Action")
            st.write(final_decision["action"])

            st.divider()

            st.subheader("Recommendation Summary")

            st.write(
                f"""
                The process has an estimated automation suitability score of **{round(suitability_score, 1)}/100**.

                The recommended automation approach is **{recommendation}** with **{round(recommendation_confidence, 1)}% confidence**.

                The expected implementation complexity is **{complexity}** with **{round(complexity_confidence, 1)}% confidence**.

                The predicted business value potential is **{business_value}** with **{round(business_value_confidence, 1)}% confidence**.
                """
            )

            st.divider()

            st.subheader("Explanation")

            st.write(explanation["score_summary"])

            st.markdown("#### Key Reasons")
            for reason in explanation["score_reasons"]:
                st.write(f"- {reason}")

            st.markdown("#### Recommendation Reason")
            st.write(explanation["recommendation_reason"])

            st.markdown("#### Suggested Next Action")
            st.success(explanation["next_action"])

            st.divider()

            st.subheader("Prediction Confidence Breakdown")

            confidence_data = pd.DataFrame({
                "Prediction Type": [
                    "Automation Recommendation",
                    "Implementation Complexity",
                    "Business Value Potential"
                ],
                "Predicted Class": [
                    recommendation,
                    complexity,
                    business_value
                ],
                "Confidence": [
                    f"{round(recommendation_confidence, 1)}%",
                    f"{round(complexity_confidence, 1)}%",
                    f"{round(business_value_confidence, 1)}%"
                ]
            })

            st.dataframe(confidence_data, use_container_width=True)

            with st.expander("View Detailed Model Probabilities"):

                recommendation_probability_table = pd.DataFrame({
                    "Automation Type": recommendation_model.classes_,
                    "Probability": recommendation_probabilities
                }).sort_values(by="Probability", ascending=False)

                recommendation_probability_table["Probability"] = (
                    recommendation_probability_table["Probability"] * 100
                ).round(1).astype(str) + "%"

                st.markdown("#### Automation Recommendation Probabilities")
                st.dataframe(recommendation_probability_table, use_container_width=True)

                complexity_probability_table = pd.DataFrame({
                    "Complexity": complexity_model.classes_,
                    "Probability": complexity_probabilities
                }).sort_values(by="Probability", ascending=False)

                complexity_probability_table["Probability"] = (
                    complexity_probability_table["Probability"] * 100
                ).round(1).astype(str) + "%"

                st.markdown("#### Implementation Complexity Probabilities")
                st.dataframe(complexity_probability_table, use_container_width=True)

                business_value_probability_table = pd.DataFrame({
                    "Business Value": business_value_model.classes_,
                    "Probability": business_value_probabilities
                }).sort_values(by="Probability", ascending=False)

                business_value_probability_table["Probability"] = (
                    business_value_probability_table["Probability"] * 100
                ).round(1).astype(str) + "%"

                st.markdown("#### Business Value Probabilities")
                st.dataframe(business_value_probability_table, use_container_width=True)

        with tabs[2]:
            st.subheader("ROI Estimation")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total Initial Investment",
                    f"${roi_estimate['total_initial_investment']:,.2f}"
                )

                st.metric(
                    "Hours Saved Per Year",
                    f"{roi_estimate['hours_saved_per_year']} hrs"
                )

                st.metric(
                    "Direct Labour Savings",
                    f"${roi_estimate['direct_labour_savings']:,.2f}"
                )

                st.metric(
                    "Indirect Savings",
                    f"${roi_estimate['indirect_savings']:,.2f}"
                )

            with col2:
                st.metric(
                    "Gross Annual Savings",
                    f"${roi_estimate['gross_annual_savings']:,.2f}"
                )

                st.metric(
                    "Net Annual Savings",
                    f"${roi_estimate['net_annual_savings']:,.2f}"
                )

                if roi_estimate["payback_period_months"] is None:
                    st.metric(
                        "Payback Period",
                        "Not applicable"
                    )
                else:
                    st.metric(
                        "Payback Period",
                        f"{roi_estimate['payback_period_months']} months"
                    )

                st.metric(
                    "Projected ROI",
                    f"{roi_estimate['roi_percent']}%"
                )

            st.caption(
                "ROI = Net Annual Savings / Total Initial Investment × 100. Estimates should be validated with real operational and financial data."
            )

            st.divider()

            st.subheader("Enterprise Automation Readiness")

            st.metric(
                "Automation Readiness Score",
                f"{readiness_assessment['score']}%"
            )

            level = readiness_assessment["level"]

            if "Level 1" in level or "Level 2" in level:
                st.error(level)
            elif "Level 3" in level:
                st.warning(level)
            else:
                st.success(level)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Readiness Strengths")

                for item in readiness_assessment["strengths"]:
                    st.write(f"- {item}")

            with col2:
                st.markdown("#### Readiness Weaknesses")

                for item in readiness_assessment["weaknesses"]:
                    st.write(f"- {item}")

            st.markdown("#### Recommended Readiness Action")
            st.info(readiness_assessment["recommended_action"])

        with tabs[3]:
            st.subheader("Enterprise Risk Assessment")

            risk_table = []

            for risk_name, risk_data in risk_summary.items():
                risk_table.append({
                    "Risk Type": risk_name,
                    "Risk Score": risk_data["score"],
                    "Risk Level": risk_data["label"]
                })

            risk_df = pd.DataFrame(risk_table)

            st.dataframe(risk_df, use_container_width=True)

            for risk_name, risk_data in risk_summary.items():

                label = risk_data["label"]
                score = risk_data["score"]

                if label == "Low":
                    st.success(f"{risk_name}: {label} ({score}/10)")
                elif label == "Medium":
                    st.warning(f"{risk_name}: {label} ({score}/10)")
                else:
                    st.error(f"{risk_name}: {label} ({score}/10)")

            st.divider()

            st.subheader("Explainable AI: Suitability Score Drivers")

            st.write(
                "This section shows which process features influenced the automation suitability score."
            )

            shap_display = shap_explanation.copy()

            shap_display["SHAP Value"] = shap_display["SHAP Value"].round(3)
            shap_display["Absolute Impact"] = shap_display["Absolute Impact"].round(3)

            with st.expander("View Detailed SHAP Explanation", expanded=True):
                st.dataframe(
                    shap_display[
                        ["Feature", "Impact Direction", "SHAP Value", "Absolute Impact"]
                    ],
                    use_container_width=True
                )

                top_positive = shap_display[shap_display["SHAP Value"] > 0].head(5)
                top_negative = shap_display[shap_display["SHAP Value"] < 0].head(5)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Top Score Increasing Factors")

                    if top_positive.empty:
                        st.write("No strong positive score drivers detected.")
                    else:
                        for _, row in top_positive.iterrows():
                            st.success(
                                f"{row['Feature']} increased the score by {row['SHAP Value']}"
                            )

                with col2:
                    st.markdown("#### Top Score Reducing Factors")

                    if top_negative.empty:
                        st.write("No strong negative score drivers detected.")
                    else:
                        for _, row in top_negative.iterrows():
                            st.warning(
                                f"{row['Feature']} reduced the score by {abs(row['SHAP Value'])}"
                            )

            st.markdown("#### Feature Impact Chart")

            chart_data = shap_display.set_index("Feature")["Absolute Impact"]

            st.bar_chart(chart_data)

            st.divider()

            st.subheader("Additional Risk Explanation")

            st.markdown("#### Risks")
            for risk in explanation["risks"]:
                st.write(f"- {risk}")

            st.markdown("#### Human Review Areas")
            for area in explanation["human_review_areas"]:
                st.write(f"- {area}")

        with tabs[4]:
            st.subheader("Export Assessment")

            st.write(
                "Download the automation assessment report for stakeholder review."
            )

            st.download_button(
                label="Download Report",
                data=assessment_report,
                file_name="automation_assessment_report.pdf",
                mime="application/pdf"
            )

else:
    with tabs[0]:
        st.info("Enter process details in the sidebar and click Analyse Process to generate the assessment.")

    with tabs[1]:
        st.info("Prediction results will appear here after analysis.")

    with tabs[2]:
        st.info("ROI and readiness results will appear here after analysis.")

    with tabs[3]:
        st.info("Risk and explainability results will appear here after analysis.")

    with tabs[4]:
        st.info("The PDF report download will appear here after analysis.")


st.divider()

st.caption(
    "AI Automation Intelligence Platform | Prototype Enterprise Automation Assessment System"
)