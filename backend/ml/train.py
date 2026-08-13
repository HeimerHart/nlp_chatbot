from __future__ import annotations

import pathlib
import sys

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from utils.text_utils import normalize

_HERE = pathlib.Path(__file__).parent
_DATA_PATH = _HERE / "data" / "pro_support_training_dataset.xlsx"
_ARTIFACT_PATH = _HERE / "artifacts" / "intent_model.joblib"


def load_dataset() -> pd.DataFrame:
    if not _DATA_PATH.exists():
        raise FileNotFoundError(
            f"Training data not found at {_DATA_PATH}. Make sure "
            "pro_support_training_dataset.xlsx is in backend/ml/data/."
        )
    df = pd.read_excel(_DATA_PATH)
    missing = {"text", "intent"} - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing expected column(s): {missing}")

    df = df.dropna(subset=["text", "intent"]).copy()
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() > 0]
    return df


def build_pipeline() -> Pipeline:
    vectorizer = TfidfVectorizer(
        preprocessor=normalize,
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True,
    )
    classifier = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
    )
    return Pipeline([("tfidf", vectorizer), ("clf", classifier)])


def main() -> None:
    df = load_dataset()
    print(f"Loaded {len(df)} labeled examples across {df['intent'].nunique()} intents.")
    print(df["intent"].value_counts().to_string())

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["intent"],
        test_size=0.2,
        random_state=42,
        stratify=df["intent"],
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("\nHeld-out evaluation (20% split):\n")
    print(classification_report(y_test, y_pred))

    pipeline.fit(df["text"], df["intent"])

    _ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, _ARTIFACT_PATH)
    print(f"\nSaved trained pipeline to {_ARTIFACT_PATH}")


if __name__ == "__main__":
    main()
