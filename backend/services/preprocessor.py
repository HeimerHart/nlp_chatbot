import re
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class NLPPreprocessor:

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer()

    


    def clean_text(self, text):

        text = text.lower()

        text = re.sub(r'[^a-zA-Z\s]', '', text)

        return text
    



    def tokenize(self, text):

        return word_tokenize(text)
    



    def remove_stopwords(self, tokens):

        return [
            word
            for word in tokens
            if word not in self.stop_words
        ]
    



    def lemmatize(self, tokens):

        doc = self.nlp(" ".join(tokens))

        return [
            token.lemma_
            for token in doc
        ]




    def extract_features(self, texts):

        return self.vectorizer.fit_transform(texts)




    def preprocess(self, text):

        text = self.clean_text(text)

        tokens = self.tokenize(text)

        tokens = self.remove_stopwords(tokens)

        tokens = self.lemmatize(tokens)
        #return " ".join(tokens)
        return tokens
    



processor = NLPPreprocessor()

result = processor.preprocess(
    "Hello! I want to return my orders."
)

#print(result)


queries = [
    "refund order",
    "track order",
    "hello"
]

features = processor.extract_features(queries)
#print(features)