import joblib

model = joblib.load(
    "backend/models/intent_classifier.pkl"
)

vectorizer = joblib.load(
    "backend/models/tfidf_vectorizer.pkl"
)

query = [
    "eh"
]

vector = vectorizer.transform(
    query
)

prediction = model.predict(
    vector
)

print(prediction[0])