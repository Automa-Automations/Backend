import json
from typing import Optional, Any

import instagrapi
from ollama import Client

from src.Classes.Bot import Bot
from src.Classes.Bots.Platforms.Instagram.Configuration import InstagramBotConfiguration
from src.Classes.ContentGenerationBotHandler import ContentGenerationBotHandler
from src.utils import insert_value, update_value
from src.Classes.Enums import BotType, Platform
from enum import Enum
from src.Classes.Bots.BotTypes.AIImageGenerator import AiImageGenerationBotMetadata, AIImageGenerationBotHandler
from src.Classes.Bots.Platforms.Instagram.Configuration import InstagramBotConfiguration
import datetime
import uuid


class InstagramPlatformBot(Bot):
    """InstagramPlatformBot: The Instagram platform bot class. This class will provide all of the methods to interact with instagram. Following & subclassing from Bot. But having its own api implementation, and other methods which are platform specific, but still shares the handler logic between different types of bots."""
    bot_configuration: InstagramBotConfiguration
    """InstagramBotConfiguration: The configuration of the bot."""

    handler: ContentGenerationBotHandler
    """ContentGenerationBotHandler: The handler of the bot."""

    _client: Optional[Client]
    _is_authenticated: bool = False
    """Client: The Private Instagrapi Client"""

    def upload(self) -> None:
        posts = self.handler.generate(owner=self.owner[1])
        print(posts)
        for post in posts:
            print(self.client.photo_upload(path=post.content, caption=f"{post.title} {' '.join(post.tags)}\n\n{post.description}").dict())
        return None

    @property
    def client(self) -> Client:
        """Client: The client of the bot."""
        if not getattr(self, "_client", None):
            self._client = instagrapi.Client()

        if self._is_authenticated:
            return self._client

        cl = self._client
        session = self.session
        cl.set_proxy(self.proxy.url)
        session_filepath = f"/tmp/{self.id}.json"
        if not session.metadata_dict['cookies']:
            cl.login(session.metadata_dict['username'], session.metadata_dict['password'])
            cl.dump_settings(session_filepath)

            with open(session_filepath, "r") as f:
                content = json.load(f)
                self.session.update(content)

        else:
            with open(session_filepath, "w") as f:
                json.dump(session.metadata_dict['cookies'], f)

            cl.load_settings(session_filepath)

        self._is_authenticated = True
        self._client = cl
        return self._client

    @staticmethod
    def new(friendly_name: str, description: str, owner_id: str, bot_type: BotType, platform: Platform, metadata_dict: dict, bot_configuration_dict: dict, session_id: int, proxy_id: int, currently_active: bool) -> Any:

        id = str(uuid.uuid4().hex)
        created_at = datetime.datetime.now()
        # bot = Bot(id=id, created_at=created_at, friendly_name=friendly_name, description=description, owner_id=owner_id, bot_type=bot_type, platform=platform, metadata_dict=metadata_dict, bot_configuration_dict=bot_configuration_dict, session_id=session_id, proxy_id=proxy_id, currently_active=currently_active)       
        if platform == Platform.Instagram:
            bot = InstagramPlatformBot(id=id, created_at=created_at, friendly_name=friendly_name, description=description, owner_id=owner_id, bot_type=bot_type, platform=platform, metadata_dict=metadata_dict, bot_configuration_dict=bot_configuration_dict, session_id=session_id, proxy_id=proxy_id, currently_active=currently_active)
        else:
            bot = Bot(id=id, created_at=created_at, friendly_name=friendly_name, description=description, owner_id=owner_id, bot_type=bot_type, platform=platform, metadata_dict=metadata_dict, bot_configuration_dict=bot_configuration_dict, session_id=session_id, proxy_id=proxy_id, currently_active=currently_active)
            
        # Create a 100% dict version of the bot
        bot_dict = bot.__dict__

        del bot_dict['configuration']
        del bot_dict['metadata']
        del bot_dict['id']

        for key, value in bot_dict.items():
            if isinstance(value, Enum):
                bot_dict[key] = value.value

            if isinstance(value, datetime.datetime):
                bot_dict[key] = value.isoformat()

        id = insert_value("bots", bot_dict)
        bot.id = id

        if bot_type == BotType.AiImageGeneration:
            bot.handler = AIImageGenerationBotHandler(metadata=AiImageGenerationBotMetadata(**metadata_dict))

        # Register the cron_jobs for the bot
        if platform == Platform.Instagram:
            bot.configuration = InstagramBotConfiguration(**bot_configuration_dict)

        for key, value in bot_configuration_dict.items():
            if "_interval" in key and "cron_job" not in key:
                cron_id = bot._create_cron(bot.id, value, key)
                setattr(bot.configuration, f"cron_job_{key}", cron_id)
                setattr(bot.configuration, key, value)

        # Now we need to update the values
        bot.bot_configuration_dict = bot.configuration.__dict__
        update_value("bots", bot.id, "bot_configuration_dict", bot.bot_configuration_dict)

            
        return bot

    @staticmethod
    def from_id(id: int, type_: Any):
        value = get_value("bots", id)
        out = type_(**value)
        # Loop over all of the bot_types to assign the ContentGenerationBotHandler
        print(out.bot_type)
        if out.bot_type == BotType.AiImageGeneration.value:
            out.handler = AIImageGenerationBotHandler(metadata=AiImageGenerationBotMetadata(**out.metadata_dict))

        if out.platform == Platform.Instagram.value:
            out.configuration = InstagramBotConfiguration(**out.bot_configuration_dict)

        return out
    def follow(self) -> None:
        """Do following logic here"""
        print("Following...")
        return None

    def follow_for_follow(self) -> None:
        """Do follow for follow logic here. Checking the schedule and more. We will allow for heavy cron interaction between the api & lambdas. Will also run on different lambdas for each of these!"""
        print("Follow for follow...")

    def make_comment(self) -> None:
        """Do make comment logic here"""
        print("Making comment...")

    def reply_to_comment(self) -> None:
        """Do reply to comment logic here"""
        print("Replying to comment...")

    def like_post(self) -> None:
        """Do like post logic here"""
        print("Liking post...")

    def comment_dm_promotion(self) -> None:
        """Do comment dm promotion logic here"""
        print("Commenting dm promotion...")
