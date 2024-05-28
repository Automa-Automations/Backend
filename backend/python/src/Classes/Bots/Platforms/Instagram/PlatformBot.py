import json
from typing import Optional

import instagrapi
from ollama import Client

from src.Classes.Bot import Bot
from src.Classes.Bots.Platforms.Instagram.Configuration import InstagramBotConfiguration
from src.Classes.ContentGenerationBotHandler import ContentGenerationBotHandler


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
