# ChatBot -- AI Customer Support Chatbot

An AI-powered customer support chatbot built with React (frontend) and FastAPI (backend).
Uses a Naive Bayes + TF-IDF intent classifier, spaCy NER, and FAQ fuzzy-matching to answer
customer queries, with a full auth system and an admin dashboard.

Credentials:
admin@chatbot.com
Admin@123

user@chatbot.com
user@123

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- A **MongoDB** database -- either a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
  cluster, or MongoDB running locally.

---

## 1. Backend setup

```bash
cd backend
python -m venv venv

# Activate it:
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### Configure environment variables

Copy the example env file and fill in your own values:

```bash
cp .env.example .env      # macOS/Linux
copy .env.example .env    # Windows
```

Edit `.env`:

```
APP_NAME=AI Customer Support Chatbot
DEBUG=True
PORT=8000
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster-host>/?appName=NLPchatbot
DATABASE_NAME=chatbot_db
JWT_SECRET_KEY=<a long random string -- do NOT keep the placeholder>
JWT_ALGORITHM=HS256
```

Generate a JWT secret with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Seed the database

Creates the sample intents and the default admin account:

```bash
python -m database.seed
```

### Run the backend

```bash
python main.py
```

Server runs at `http://localhost:8000`.

> **Known first-run issue:** if chat messages fail with a generic "Something went wrong"
> error, NLTK is missing the `punkt_tab` tokenizer resource. This project's
> `services/preprocessor.py` downloads it automatically on startup, but if your NLTK
> cache is already partially populated from a previous install, run this once manually:
>
> ```bash
> python -c "import nltk; nltk.download('punkt_tab')"
> ```

---

## 2. Frontend setup

In a **second** terminal:

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`.

---

## 3. Logging in

**Admin** (created automatically by the seed script):

```
Email:    admin@chatbot.com
Password: Admin@123
```

Logging in with this account routes straight to the admin dashboard: users, intents,
conversation logs, and analytics.

Change or remove this password before deploying anywhere public -- it's a seed-only
default.

**Regular user:** click "Create an account" on the login page and sign up with any
email + a password of 6+ characters. This drops you into the chat UI instead.

---

## 4. Using the chatbot

- Type a message and send -- it's routed through FAQ fuzzy-matching first, then a
  Naive Bayes + TF-IDF intent classifier with spaCy NER for entity extraction
  (order IDs, dates, locations, products).
- Chat history is saved per-session and reloads automatically next time you log in.
- The chatbot only recognizes intents seeded in `backend/database/seed.py`
  (greetings, refunds, order status/cancel, etc.) -- anything outside that scope gets
  a generic fallback reply. Add more intents there (and re-run the seed script) to
  expand what it understands.

---

## Project structure

```
backend/
  controllers/     # request handlers (auth, chat)
  routes/          # FastAPI route definitions
  services/        # NLP pipeline: preprocessing, intent classifier, NER, FAQ matching
  models/          # trained ML artifacts (.pkl) and Mongo schemas
  database/        # Mongo connection + seed script
  middleware/      # auth / admin guards
frontend/
  src/
    Login.jsx          # sign in / sign up
    chatbot.jsx         # main chat UI
    AdminDashboard.jsx  # admin panel
    AnalyticsDashboard.jsx
    api.js              # axios client + session handling
```
