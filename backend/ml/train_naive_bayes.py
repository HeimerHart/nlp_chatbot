import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report



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

X_train = vectorizer.fit_transform(X_train)

X_test = vectorizer.transform(X_test)



model = MultinomialNB()

model.fit(
    X_train,
    y_train
)


predictions = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Accuracy: {accuracy:.2f}"
)



print(
    classification_report(
        y_test,
        predictions
    )
)


joblib.dump(
    model,
    "backend/models/naive_bayes_classifier.pkl"
)

joblib.dump(
    vectorizer,
    "backend/models/nb_vectorizer.pkl"
)




from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, predictions)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

disp.plot()
plt.title("Naive Bayes Confusion Matrix")
plt.show()
