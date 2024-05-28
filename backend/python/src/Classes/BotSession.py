from dataclasses import dataclass
import datetime
from typing import Tuple
from src.Classes.Enums import Platform
from src.Classes.User import Profile, DatabaseSyncedProfile
from src.utils import get_value, update_value


@dataclass
class BotSession:
    id: str
    """str: The unique identifier for the session of the bot."""

    created_at: datetime.datetime
    """datetime.datetime: The date this bot_session was created!"""

    platform: Platform
    """Platform: The platform of the bot. This will define the schema for 'Bot().bot_configuration'."""

    owner_id: str
    """str: The unique identifier for the owner of the bot."""

    metadata_dict: dict
    """dict: The metadata of the bot."""

    @property
    def owner(self) -> Tuple[Profile, DatabaseSyncedProfile]:
        """Tuple[Profile, DatabaseSyncedProfile]: The owner of the bot. Useful for modifying the user account based on bot actions."""
        return (Profile.from_id(self.owner_id), DatabaseSyncedProfile.from_id(self.owner_id))

    @staticmethod
    def from_dict(dict_: dict):
        return BotSession(**dict_)

    @staticmethod
    def from_id(id: int):
        table = "bot_sessions"
        value = get_value(table=table, line=id)
        return BotSession.from_dict(value)

    def update(self, new_metadata):
        table = "bot_sessions"
        # Take the current metadata
        current_metadata = self.metadata_dict
        # add the cookies
        current_metadata['cookies'] = new_metadata
        update_value(table=table, line=self.id, val="metadata_dict", new_value=current_metadata)


