import joblib

model = joblib.load(
    "models/naive_bayes_classifier.pkl"
)

vectorizer = joblib.load(
    "models/nb_vectorizer.pkl"
)

def predict_intent(text):

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)

    return prediction[0]