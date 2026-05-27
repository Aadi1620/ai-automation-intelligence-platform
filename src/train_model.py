import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "synthetic_process_dataset.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

feature_columns = [
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

X = df[feature_columns]

score_target = df["automation_suitability_score"]
recommendation_target = df["automation_recommendation"]
complexity_target = df["implementation_complexity"]
business_value_target = df["business_value_potential"]


def train_score_model():
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        score_target,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print("Suitability Score Model")
    print("Mean Absolute Error:", round(mae, 2))

    joblib.dump(model, MODEL_DIR / "score_model.pkl")


def train_classification_model(target, file_name, display_name):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print()
    print(display_name)
    print("Accuracy:", round(accuracy_score(y_test, predictions), 2))
    print(classification_report(y_test, predictions))

    joblib.dump(model, MODEL_DIR / file_name)


if __name__ == "__main__":
    train_score_model()

    train_classification_model(
        recommendation_target,
        "recommendation_model.pkl",
        "Automation Recommendation Model"
    )

    train_classification_model(
        complexity_target,
        "complexity_model.pkl",
        "Implementation Complexity Model"
    )

    train_classification_model(
        business_value_target,
        "business_value_model.pkl",
        "Business Value Model"
    )

    print()
    print("Training completed. Final models saved in the models folder.")