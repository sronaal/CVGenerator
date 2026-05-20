import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def clean_bullet(bullet: str) -> str:
    bullet = bullet.strip()
    bullet = re.sub(r"^[\-\*\•\u2022\u2013\u2014]\s*", "", bullet)
    bullet = clean_text(bullet)
    if bullet and not bullet.endswith("."):
        bullet += "."
    return bullet


def clean_bullets(bullets: list[str]) -> list[str]:
    return [clean_bullet(b) for b in bullets if b.strip()]
