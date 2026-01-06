from abc import ABC, abstractmethod
from re import Pattern
from typing import TypedDict

from .utils import get_url_without_scheme


class DeepLinkUrls(TypedDict):
    web: str
    ios: str
    android: str


class HandlerMatch(TypedDict):
    pass


class HandlerType[T](ABC):
    name: str
    patterns: list[Pattern[str]] | list[tuple[str, Pattern[str]]]
    url: str

    def __init__(self, url: str):
        self.url = get_url_without_scheme(url)

    @abstractmethod
    def match_pattern(self) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def generate_url(self, match_result: T) -> DeepLinkUrls:
        raise NotImplementedError
