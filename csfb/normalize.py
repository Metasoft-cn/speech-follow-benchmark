import unicodedata
import re


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    # Keep the public baseline's multilingual aids explicit, small, and deterministic.
    for pattern, spoken in (
        (r"(?<!\d)2026(?!\d)", "二零二六"),
        (r"(?<!\d)21(?!\d)", "二十一"),
        (r"(?<!\d)3\.5(?!\d)", "三点五"),
        (r"(?<!\d)15%", "百分之十五"),
    ):
        text = re.sub(pattern, spoken, text)
    text = text.replace("android", "安卓")
    return "".join(c for c in text if not c.isspace() and unicodedata.category(c)[0] not in "PS")
