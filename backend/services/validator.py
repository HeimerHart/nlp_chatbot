import re

def sanitize(text):

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    return text.strip()