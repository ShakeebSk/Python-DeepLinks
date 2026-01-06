import re


def get_url_without_scheme(url: str) -> str:
    return re.sub(r"^https?://", "", url)
