import joblib

model = joblib.load(
    "backend/models/naive_bayes_classifier.pkl"
)

vectorizer = joblib.load(
    "backend/models/nb_vectorizer.pkl"
)

query = ["hi"]

query_vector = vectorizer.transform(query)

prediction = model.predict(query_vector)

print(prediction[0])