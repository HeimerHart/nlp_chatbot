import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score

import joblib

df = pd.read_csv(
    "backend/datas/training_dataset.csv"


)

X = df["text"]

y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(
    X_train
)

X_test = vectorizer.transform(
    X_test
)

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train,
    y_train
)


predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Accuracy: {accuracy:.2f}"
)




joblib.dump(
    model,
    "backend/models/intent_classifier.pkl"
)

joblib.dump(
    vectorizer,
    "backend/models/tfidf_vectorizer.pkl"
)

print("Model saved")