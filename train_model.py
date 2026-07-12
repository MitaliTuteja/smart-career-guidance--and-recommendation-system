import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier


df = pd.read_csv("Dataset.csv")

features = [
    "Academic Score",
    "Stream",
    "Technical Skill",
    "Soft Skill",
    "Personality",
    "Interest",
    "Work Style"
]

target = "Career Domain"

X = df[features]
y = df[target]

target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

categorical_features = [
    "Stream",
    "Technical Skill",
    "Soft Skill",
    "Personality",
    "Interest",
    "Work Style"
]

numeric_features = ["Academic Score"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

rf_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42))
])

xgb_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        eval_metric="mlogloss"
    ))
])

rf_pipeline.fit(X_train, y_train)
rf_pred = rf_pipeline.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

xgb_pipeline.fit(X_train, y_train)
xgb_pred = xgb_pipeline.predict(X_test)
xgb_accuracy = accuracy_score(y_test, xgb_pred)

print("Random Forest Accuracy:", round(rf_accuracy * 100, 2), "%")
print("XGBoost Accuracy:", round(xgb_accuracy * 100, 2), "%")

if rf_accuracy >= xgb_accuracy:
    best_model = rf_pipeline
    best_model_name = "Random Forest"
    best_accuracy = rf_accuracy
else:
    best_model = xgb_pipeline
    best_model_name = "XGBoost"
    best_accuracy = xgb_accuracy

print("Best Model:", best_model_name)
print("Best Accuracy:", round(best_accuracy * 100, 2), "%")

with open("career_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("target_encoder.pkl", "wb") as f:
    pickle.dump(target_encoder, f)

print("Model saved successfully.")