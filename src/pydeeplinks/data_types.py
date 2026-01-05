from abc import ABC, abstractmethod
from re import Pattern
from typing import Generic, TypedDict, TypeVar

from .utils import get_url_without_scheme


class DeepLinkUrls(TypedDict):
    web: str
    ios: str
    android: str


class HandlerMatch(TypedDict):
    pass


T = TypeVar("T", bound=HandlerMatch)


class HandlerType(ABC, Generic[T]):
    name: str
    patterns: list[Pattern[str]]
    url: str

    def __init__(self, url: str):
        self.url = get_url_without_scheme(url)

    @abstractmethod
    def match_pattern(self) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def generate_url(self, match_result: T) -> DeepLinkUrls:
        raise NotImplementedError
