# TODO: Make every class have a "DatabaseSynced" variant if applicable.
# TODO: Refactor all the code into the correct place.

import datetime
import traceback
import requests
import os

from dataclasses import dataclass
from typing import Tuple, Any, Optional
from src.Classes.BotSession import BotSession
from src.utils import update_value
from src.Classes.User import Profile, DatabaseSyncedProfile
from src.Classes.Proxy import Proxy
from src.Classes.Enums import BotType, Platform



@dataclass
class Bot:
    id: str
    """str: The unique identifier for the bot."""

    created_at: datetime.datetime
    """datetime.datetime: The date and time the bot was created."""

    owner_id: str
    """str: The unique identifier for the owner of the bot."""

    friendly_name: str
    """str: The friendly name of the bot."""

    description: str
    """str: The description of the bot."""

    proxy_id: int
    """int: The unique identifier for the proxy of the bot."""

    metadata_dict: dict
    """dict: The metadata of the bot."""

    bot_type: BotType
    """BotType: The type of the bot. This will define the schema for 'Bot().metadata'"""

    bot_configuration_dict: dict
    """dict: The configuration of the bot."""

    platform: Platform
    """Platform: The platform of the bot. This will define the schema for 'Bot().bot_configuration'."""

    session_id: int
    """int: The unique identifier for the session of the bot. This is used to authenticate the bot. Because a single `SocialAccount` can have multiple bots, the session_id will provide us with the information required"""

    currently_active: bool
    """bool: If the bot is currently active or not."""

    metadata: None = None
    """None: The metadata of the bot. This will be defined in the subclass."""

    configuration: None = None
    """None: The configuration of the bot. This will be defined in the subclass."""

    @property
    def owner(self) -> Tuple[Profile, DatabaseSyncedProfile]:
        """Tuple[Profile, DatabaseSyncedProfile]: The owner of the bot. Useful for modifying the user account based on bot actions."""
        return (
            Profile.from_id(self.owner_id),
            DatabaseSyncedProfile.from_id(self.owner_id),
        )

    @property
    def proxy(self) -> Proxy:
        """Proxy: The proxy of the bot. Useful for modifying the proxy based on bot actions."""
        return Proxy.from_id(self.proxy_id)

    @property
    def session(self) -> BotSession:
        """Session: The session of the bot. Useful for modifying the session based on bot actions. The session is just a dictionary!"""
        return BotSession.from_id(self.session_id)

    @staticmethod
    def from_id(id: int, type_: Any):
        # value = get_value("bots", id)
        # out = type_(**value)
        # # Loop over all of the bot_types to assign the ContentGenerationBotHandler
        # print(out.bot_type)
        # if out.bot_type == BotType.AiImageGeneration.value:
        #     out.handler = AIImageGenerationBotHandler(metadata=AiImageGenerationBotMetadata(**out.metadata_dict))
        #
        # if out.platform == Platform.Instagram.value:
        #     out.configuration = InstagramBotConfiguration(**out.bot_configuration_dict)
        #
        # return out
        pass

    @staticmethod
    def new(
        friendly_name: str,
        description: str,
        owner_id: str,
        bot_type: BotType,
        platform: Platform,
        metadata_dict: dict,
        bot_configuration_dict: dict,
        session_id: int,
        proxy_id: int,
        currently_active: bool,
    ) -> Any:
        """new: This method will create a new bot."""
        pass
      
    def modify_schedule(self, name: str, new_value: str) -> None:
        """modify_schedule: This method will modify the schedule of the bot."""
        # Firstly we convert the configuration to a dictionary
        # All we need to do is make evenbridge take in the bot_id & the name of the property in order to make all of it's desired changes.
        if not self.configuration:
            raise Exception("No configuration found for the bot!")

        # If there is an existing cron indicated by the _cron_job_{name} attr
        existing_cron = getattr(self.configuration, f"cron_job_{name}", None)
        if existing_cron:
            self._delete_schedule(cron_id=existing_cron)

        # Now create the cron
        cron_id = self._create_cron(self.id, new_value, name)
        # Now we update the configuration fully
        setattr(self.configuration, f"cron_job_{name}", cron_id)
        setattr(self.configuration, name, new_value)
        # Now we need to update the value
        self.bot_configuration_dict = self.configuration.__dict__
        update_value(
            "bots", self.id, "bot_configuration_dict", self.bot_configuration_dict
        )

    @staticmethod
    def _create_cron(bot_id: str, cron: str, cron_name: str) -> Optional[dict]:
        api_base_url = (
            os.environ["API_BASE_URL"] + "/run_cron_job"
        )  # This is because a ton of the code will be super generic for this first version as it makes us build way faster!
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer  {os.environ.get("CRON_JOBS_ORG_API_KEY")}',
            }

            values = cron.split(" ")
            new_values = []
            for value in values:
                cleaned_value = value.strip()
                if cleaned_value == "*":
                    cleaned_value = ["-1"]
                elif "," in cleaned_value and isinstance(cleaned_value, str):
                    cleaned_value = cleaned_value.split(",")
                else:
                    cleaned_value = [cleaned_value]

                cleaned_value = [int(x) for x in cleaned_value]
                new_values.append(cleaned_value)

            json_data = {
                "job": {
                    "url": f"{api_base_url}/?bot_id={bot_id}&cron_name={cron_name}",
                    "enabled": "true",
                    "saveResponses": True,
                    "schedule": {
                        "timezone": "Europe/Berlin",
                        "expiresAt": 0,
                        "hours": new_values[1],
                        "mdays": new_values[2],
                        "minutes": new_values[0],
                        "months": new_values[3],
                        "wdays": new_values[4],
                    },
                },
            }

            response = requests.put(
                "https://api.cron-job.org/jobs", headers=headers, json=json_data
            )
            return response.json()["jobId"]
        except Exception as e:
            print(e, traceback.format_exc())
            return None

    @staticmethod
    def _delete_schedule(cron_id: str):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {os.environ.get("CRON_JOB_ORG_API")}',
            }

            requests.delete(f"https://api.cron-job.org/jobs/{cron_id}", headers=headers)
            return True
        except Exception as e:
            print(e)
            return False
