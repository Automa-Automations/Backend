from dataclasses import dataclass
from typing import Any, List

from src.Classes.User import DatabaseSyncedProfile


@dataclass
class ContentGenerationBotHandler():
    """ContentGenerationBotHandler: The Content Generation bot class. This class"""

    metadata: Any
    """None: The metadata of the bot."""

    def generate(self, owner: DatabaseSyncedProfile) -> List['Post']:
        """generate: This method will generate the content using the metadata of the bot."""
        return []

    @classmethod
    def from_type(cls, type_: 'ContentGenerationBotHandler', metadata: Any) -> Any:
        """generate: This method will generate the content using the metadata of the bot."""
        return type_(metadata)
