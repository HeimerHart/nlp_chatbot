import spacy
import re

nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str):

    doc = nlp(text)

    entities = {}

    for ent in doc.ents:
        entities[ent.label_] = ent.text

    order = re.search(r"\b\d{4,}\b", text)

    if order:
        entities["ORDER_ID"] = order.group()

    return entities