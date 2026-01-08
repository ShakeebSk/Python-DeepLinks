from ..data_types import HandlerType
from .facebook import FacebookHandler
from .linkedin import LinkedInHandler
from .youtube import YouTubeHandler

handlers_list: list[type[HandlerType]] = [
    FacebookHandler,
    LinkedInHandler,
    YouTubeHandler,
]

__all__ = [
    "handlers_list",
    "FacebookHandler",
    "LinkedInHandler",
    "YouTubeHandler",
]
