import joblib

model = joblib.load(
    "backend/models/intent_classifier.pkl"
)

vectorizer = joblib.load(
    "backend/models/tfidf_vectorizer.pkl"
)

query = [
    "no thanks",
    "price?",
    "are you alive?"
]

vector = vectorizer.transform(
    query
)

prediction = model.predict(
    vector
)
for i, j in zip(query, prediction):
    print("Query:", i)
    print("Prediction:", j)
    print()