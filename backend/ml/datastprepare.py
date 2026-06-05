import json
import pandas as pd

with open(
    "backend/datas/intent.json",
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

rows = []

for intent_data in data["intents"]:

    intent = intent_data["intent"]

    for pattern in intent_data["text"]:

        rows.append({
            "text": pattern,
            "intent": intent
        })

df = pd.DataFrame(rows)

print(df.head())

df.to_csv(
    "backend/datas/training_dataset.csv",
    index=False
)

print("Dataset created!")
print("Total Samples:", len(df))
print("Total Intents:", df["intent"].nunique())