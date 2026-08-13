from __future__ import annotations

import re
from enum import Enum

_ANGRY_EMOJI = {"😡", "🤬", "😠"}
_DISTRESS_EMOJI = {"😭", "😢", "😞", "😔"}
_HAPPY_EMOJI = {"🙂", "😊", "😀", "😄", "❤️", "🙏"}

_URGENT_WORDS = {"asap", "urgent", "immediately", "now"}
_ANGRY_WORDS = {"angry", "furious", "ridiculous", "unacceptable", "worst"}
_DISTRESS_WORDS = {"please", "help", "worried", "scared", "stressed"}


class Tone(str, Enum):
    URGENT = "urgent"
    REASSURING = "reassuring"
    UPBEAT = "upbeat"


def detect_tone(message: str) -> Tone:
    lowered = message.lower()
    has_bang = "!!" in message or message.count("!") >= 2
    has_caps_word = bool(re.search(r"\b[A-Z]{3,}\b", message))

    if any(e in message for e in _ANGRY_EMOJI) or any(w in lowered for w in _ANGRY_WORDS):
        return Tone.URGENT
    if any(w in lowered for w in _URGENT_WORDS) or has_bang or has_caps_word:
        return Tone.URGENT
    if any(e in message for e in _DISTRESS_EMOJI) or any(w in lowered for w in _DISTRESS_WORDS):
        return Tone.REASSURING
    if any(e in message for e in _HAPPY_EMOJI):
        return Tone.UPBEAT

    return Tone.UPBEAT
