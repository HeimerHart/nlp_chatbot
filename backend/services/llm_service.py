from __future__ import annotations

import os

import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

_TIMEOUT_SECONDS = 6


def is_available() -> bool:
    return bool(GROQ_API_KEY)


def generate_reply(system_prompt: str, canned_reply: str, user_message: str) -> str | None:
    if not GROQ_API_KEY or not canned_reply.strip():
        return None

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": (
                            f"User's message: {user_message!r}\n\n"
                            "Reference reply -- keep the exact same meaning, "
                            "facts, and any bullet points/questions in it, "
                            "just phrase it more naturally and warmly. "
                            "1-4 short sentences, plain text, no markdown, "
                            "no greeting if the reference doesn't have one:\n"
                            f"{canned_reply!r}"
                        ),
                    },
                ],
                "temperature": 0.6,
                "max_tokens": 220,
            },
            timeout=_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()
        return text or None
    except Exception:
        return None
