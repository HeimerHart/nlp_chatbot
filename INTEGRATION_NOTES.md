# Integration notes

This is the full admin/login app (`nlp_chatbot_ui.zip`) with the AI model
from the demo zip (`nlp_chatbot.zip`) wired in, replacing the old
NLTK-preprocessor + Naive Bayes pipeline. Nothing else about the app
(auth, admin dashboard, analytics) changed.

## What changed

**Backend**
- `backend/ml/` — new: TF-IDF + Logistic Regression classifier trained
  on 4,900 examples across 7 intents (`ml/data/pro_support_training_dataset.xlsx`).
  The shipped `ml/artifacts/intent_model.joblib` was retrained during
  this integration so its pickled preprocessor matches this project's
  import layout (no `backend.` prefix) — reusing the demo's original
  artifact as-is would have failed to unpickle here.
- `backend/services/intent_classifier.py`, `response_service.py`,
  `tone.py`, `utils/text_utils.py`, `models/intent.py`, `datas/mock_data.py`
  — new, ported from the demo (import paths adjusted to this project's
  convention).
- `backend/controllers/chat_controller.py` — rewritten: FAQ override →
  tiny bye/thankyou pattern catch → the new classifier → response
  builder (dynamic reply + quick-reply buttons + optional card).
- `backend/database/seed.py` — the seeded `intents` collection now
  matches what the model can actually predict (was previously a
  mismatched taxonomy, the root cause of the old "I do not understand"
  spam). `responses` there is a reference sample for the admin UI only;
  live replies come from `response_service.py`.
- `backend/models/chat_model.py`, `routes/route.py`,
  `routes/conversation_route.py` — added `conversation_id` so chat
  history is threaded (ChatGPT-style), plus `/api/conversations/threads/{session_id}`
  and `/api/conversations/{session_id}/thread/{conversation_id}`.
- Removed: `services/preprocessor.py`, `services/ner_service.py`,
  `services/intentclassifier.py` (old, misspelled), old `ml/`
  naive-bayes scripts, old `.pkl` model files, old `datas/Intent.json`
  + `training_dataset.csv`.
- `requirements.txt` — added `openpyxl` (needed to read the `.xlsx`
  training set).

**Frontend**
- `src/chatbot.jsx` — rewritten: sidebar now lists conversation threads
  (not a flat message log) with a "New chat" button; bot messages
  render the model's dynamic quick-reply buttons and, for order/refund
  intents, an `OrderStatusCard` / `RefundTimelineCard`.
- `src/components/OrderStatusCard.jsx`, `RefundTimelineCard.jsx` — new.
- `src/index.css` — updated with thread-list and info-card styles.

## Running it

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in MONGODB_URI, DATABASE_NAME, JWT_SECRET_KEY
python database/seed.py   # seeds intents + creates admin@chatbot.com / Admin@123
python main.py
```

```bash
cd frontend
npm install
cp .env.example .env   # set VITE_API_URL if not localhost:8000
npm run dev
```

The model artifact is already trained and committed at
`backend/ml/artifacts/intent_model.joblib`. To retrain it:

```bash
cd backend
python -m ml.train
```
