from __future__ import annotations

import pathlib

_ARTIFACT_PATH = pathlib.Path(__file__).parent / "artifacts" / "intent_model.joblib"

_pipeline = None
_load_error: Exception | None = None

try:
    import joblib

    if _ARTIFACT_PATH.exists():
        _pipeline = joblib.load(_ARTIFACT_PATH)
except Exception as exc:
    _load_error = exc
    _pipeline = None


def is_available() -> bool:
    return _pipeline is not None


def predict_intent(text: str) -> dict[str, float]:
    if _pipeline is None or not text.strip():
        return {}

    probs = _pipeline.predict_proba([text])[0]
    labels = _pipeline.classes_
    return {label: float(p) for label, p in zip(labels, probs)}
