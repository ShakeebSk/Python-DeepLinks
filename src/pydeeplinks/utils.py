def get_url_without_scheme(url: str) -> str:
    return url.replace("https://", "").replace("http://", "")
