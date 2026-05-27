import shap
import pandas as pd


def generate_shap_explanation(model, input_data):
    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(input_data)

    if isinstance(shap_values, list):
        shap_values = shap_values[0]

    shap_df = pd.DataFrame({
        "Feature": input_data.columns,
        "SHAP Value": shap_values[0]
    })

    shap_df["Impact Direction"] = shap_df["SHAP Value"].apply(
        lambda value: "Increases Score" if value > 0 else "Reduces Score"
    )

    shap_df["Absolute Impact"] = shap_df["SHAP Value"].abs()

    shap_df = shap_df.sort_values(
        by="Absolute Impact",
        ascending=False
    )

    return shap_df