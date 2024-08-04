from dataclasses import dataclass
from typing import Any, List
from src.Classes.Enums import PostPublicity


@dataclass
class Post():
    content: Any
    """Any: The content of the post. This can be a file, a string, or anything else that is required for the post."""

    title: str
    """str: The title of the post."""

    description: str
    """str: The description of the post"""

    tags: List[str]
    """str: The tags/hashtags of the post"""

    publicity: PostPublicity
    """PostPublicity: The visibility of the post"""


