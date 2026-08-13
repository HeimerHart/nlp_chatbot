import re
import string

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    def _ensure_nltk_data():
        for pkg in ("punkt", "punkt_tab", "stopwords"):
            try:
                nltk.data.find(f"tokenizers/{pkg}")
            except LookupError:
                try:
                    nltk.data.find(f"corpora/{pkg}")
                except LookupError:
                    try:
                        nltk.download(pkg, quiet=True)
                    except Exception:
                        pass

    _ensure_nltk_data()
    _STOPWORDS = set(stopwords.words("english"))
    _NLTK_OK = True
except Exception:
    _STOPWORDS = {
        "a", "an", "the", "is", "are", "was", "were", "i", "my", "me",
        "to", "for", "of", "on", "in", "it", "and", "or", "please",
        "hi", "hello", "hey", "can", "you", "have", "has", "do", "did",
    }
    _NLTK_OK = False


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str) -> list[str]:
    normalized = normalize(text)
    if _NLTK_OK:
        try:
            return word_tokenize(normalized)
        except Exception:
            pass
    return normalized.split()


def significant_tokens(text: str) -> set[str]:
    return {t for t in tokenize(text) if t not in _STOPWORDS and len(t) > 1}
