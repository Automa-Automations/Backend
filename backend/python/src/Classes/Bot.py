# A "Bot" class is the baseclass for all other bots, each bot has a couple of paramaters that puts them into a subset of which ones we should parse them out in the switch case statement. Basically a BotFactory
import datetime
import uuid
import traceback
import requests
import os

import instagrapi
import json
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Tuple, Any, List, Optional

from ollama import Client
from src.ai.ImageApi import ImageApi
from src.utils import get_value, update_value
from src.Classes.User import Profile, DatabaseSyncedProfile
client = Client(host="http://localhost:11434")

class BotType(Enum):
    AiImageGeneration = "AiImageGeneration"

class Platform(Enum):
    Instagram = "Instagram"

class PostPublicity(Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    UNLISTED = "Unlisted"

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



@dataclass
class Proxy:
    id: int
    created_at: datetime.datetime
    host: str
    port: int
    type_: str
    security: str
    username: str
    password: str
    country: str
    
    @property
    def url(self) -> str:
        return f"{self.type_}://{self.username}:{self.password}@{self.host}:{self.port}"
    
    @property
    def requests_proxy(self) -> dict:
        return {
            "http": self.url,
            "https": self.url
        }

    @classmethod
    def from_dict(cls, dict_: dict):
        return Proxy(**dict_)

    @classmethod
    def from_id(cls, id: int):
        table = "proxies"
        value = get_value(table=table, line=id)
        return cls.from_dict(value)



@dataclass
class Bot():
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
        return (Profile.from_id(self.owner_id), DatabaseSyncedProfile.from_id(self.owner_id))
     

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
        value = get_value("bots", id)
        out = type_(**value)
        # Loop over all of the bot_types to assign the ContentGenerationBotHandler
        print(out.bot_type)
        if out.bot_type == BotType.AiImageGeneration.value:
            out.handler = AIImageGenerationBotHandler(metadata=AiImageGenerationBotMetadata(**out.metadata_dict))

        if out.platform == Platform.Instagram.value:
            out.configuration = InstagramBotConfiguration(**out.bot_configuration_dict)

        return out

    @staticmethod
    def new(friendly_name: str, description: str, owner_id: str, bot_type: BotType, platform: Platform, metadata_dict: dict, bot_configuration_dict: dict, session_id: int, proxy_id: int, currently_active: bool) -> Any:
        """new: This method will create a new bot."""
        id = str(uuid.uuid4().hex)
        created_at = datetime.datetime.now()
        # bot = Bot(id=id, created_at=created_at, friendly_name=friendly_name, description=description, owner_id=owner_id, bot_type=bot_type, platform=platform, metadata_dict=metadata_dict, bot_configuration_dict=bot_configuration_dict, session_id=session_id, proxy_id=proxy_id, currently_active=currently_active)       
        if platform == Platform.Instagram.value:
            bot = InstagramPlatformBot(id=id, created_at=created_at, friendly_name=friendly_name, description=description, owner_id=owner_id, bot_type=bot_type, platform=platform, metadata_dict=metadata_dict, bot_configuration_dict=bot_configuration_dict, session_id=session_id, proxy_id=proxy_id, currently_active=currently_active)
        else:
            bot = Bot(id=id, created_at=created_at, friendly_name=friendly_name, description=description, owner_id=owner_id, bot_type=bot_type, platform=platform, metadata_dict=metadata_dict, bot_configuration_dict=bot_configuration_dict, session_id=session_id, proxy_id=proxy_id, currently_active=currently_active)

        if bot_type == BotType.AiImageGeneration:
            bot.handler = AIImageGenerationBotHandler(metadata=AiImageGenerationBotMetadata(**metadata_dict))
        
        # TODO: Insert the bot into the database
        # TODO: Getters and setters for all of these properties (Because we want to easily update it!)
        return bot

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
        update_value("bots", self.id, "bot_configuration_dict", self.bot_configuration_dict)
        

    @staticmethod
    def _create_cron(bot_id: str, cron: str, cron_name: str) -> Optional[dict]:
        api_base_url = os.environ['API_BASE_URL'] + "/run_cron_job" # This is because a ton of the code will be super generic for this first version as it makes us build way faster!
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
            return response.json()['jobId']
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

    

@dataclass
class InstagramBotConfiguration():
    """InstagramBotConfiguration: The configuration for the Instagram bot."""
    posting_interval: str
    """str: This is the cron job used to post to the platform."""
   
    follow_for_follow: bool
    """bool: If the bot should follow for follow."""

    follow_interval: str
    """str: The cron schedule for when it should do it's follow for follow actions"""

    follow_limit: Tuple[int, int]
    """Tuple[int, int]: The minimum and maximum number of users the bot should follow. On Each iteration, the bot will follow a random number of users between the minimum and maximum."""

    reply_to_comments: bool
    """bool: If the bot should reply to comments."""

    reply_interval: str
    """str: The cron schedule for when it should reply to comments."""

    reply_limit: Tuple[int, int]
    """Tuple[int, int]: The minimum and maximum number of comments the bot should reply to. On Each iteration, the bot will reply to a random number of comments between the minimum and maximum."""

    self_like: bool
    """bool: If the bot should like its own posts, right after posting!"""

    comment_dm_promotion: bool
    """bool: If the bot should comment on other posts, to try and get a promotion in DM's"""

    comment_dm_promotion_interval: str
    """str: The cron schedule for when it should do self dm promotions."""

    comment_dm_promotion_limit: Tuple[int, int]
    """Tuple[int, int]: The minimum and maximum number of comments the bot should make to try and get a promotion in DM's. On Each iteration, the bot will comment on a random number of posts between the minimum and maximum."""

    cron_job_posting_interval: int = None
    """int: The cron-job.org jobId"""
 

@dataclass
class AiImageGenerationBotMetadata():
    """AiImageGenerationBotMetadata: The metadata for the AiImageGeneration bot."""
    model: str
    """str: The model to use for generating the image."""

    style: str
    """str: The style to use for generating the image."""

    size: Tuple[int, int]
    """str: The size of the image to generate."""

    negative_prompt: str
    """str: The negative prompt to use for generating the image."""

    positive_prompt: str
    """str: The positive prompt to use for generating the image."""

    title_prompt: str
    """str: The title prompt to use for generating the image."""

    description_prompt: str
    """str: The description prompt to use for generating the image."""

    total_images: int
    """int: The total number of images to generate."""

    base_topic: str
    """str: The base topic of the images. This is like the main driver of what should be generated!"""

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


class AIImageGenerationBotHandler(ContentGenerationBotHandler):
    """AIImageGenerationBot: The AI Image Generation bot class. This class will provide all of the methods to interact with the AI Image Generation bot."""

    metadata: AiImageGenerationBotMetadata
    """AiImageGenerationBotMetadata: The metadata of the bot."""

    def _generate_topic_item(self, base_topic: str):
        return client.generate(
            model="llama3",
            prompt=f"Please generate a 1-3 word topic based on the base_topic provided: {base_topic}. You should only respond with the response, no extra fluff attached to the message, for example <BASE_TOPIC>, your response: Cute ginger cat",
        )["response"]

    def _generate_image_prompt(self, base_prompt: str, topic: str, style: str):
        return client.generate(
            model="llama3",
            prompt=f'{base_prompt} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image prompt that will allow the AI image generator to generate a high quality image! Limit your propmpt to 2 sentences, and only respond with the image prompt, No extra context before or after, for example: MY INPUT, your output: "very cute tiny, A cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"',
        )["response"]

    def _generate_image_title(self, base_title: str, topic: str, style: str):
        return client.generate(
            model="llama3",
            prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image title that will allow the AI image generator to generate a high quality image! Limit your title to 2 sentences, and only respond with the image title, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus"',
        )["response"]

    def _generate_image_description(
        self, base_title: str, topic: str, style: str
    ):
        return client.generate(
            model="llama3",
            prompt=f'{base_title} The topic for the image should be: {topic}. And the stile reference should be {style}. Give us a descriptive image description that will allow the AI image generator to generate a high quality image! Limit your description to 10 sentences, max, and 1 sentence min, only respond with the image description, No extra context before or after, for example: MY INPUT, your output: "Cute orange cat smile wearing sweater avatar, rim lighting, adorable big eyes, small, By greg rutkowski, chibi, Perfect lighting, Sharp focus... REST OF RESPONSE ... Check out my socials ... #something, something something!"',
        )["response"]

    def _generate_image(
        self, prompt: str, negative_prompt: str, model: str, size: tuple
    ):
        api = ImageApi()
        return api.generate_image(
            prompt, negative_prompt, model, size[0], size[1]
        )

    def generate(self, owner: DatabaseSyncedProfile) -> List['Post']:
        posts = []
        for i in range(self.metadata.total_images): 
            # It costs 1 credit per image
            if  owner.credits < 1:
                raise Exception("Not enough credits to generate images!")

            owner.credits -= 1

            print("Generating topic...")
            topic = self._generate_topic_item(self.metadata.base_topic)
            print("Generated topic: ", topic)

            print("Generating prompt...")
            prompt = self._generate_image_prompt(
                self.metadata.positive_prompt, topic, self.metadata.style
            )
            print("Generated prompt: ", prompt)
        
            print("Generating title...")
            title = self._generate_image_title(
                self.metadata.title_prompt
                + f"Here is the prompt for the generated image, you can also use this as reference! {prompt}".format(
                    prompt=prompt
                ),
                topic,
                self.metadata.style,
            )
            print("Generated title: ", title)
        
            print("Generating description...")
            description = self._generate_image_description(
                title,
                topic + "\nImage Prompt: {prompt}".format(prompt=prompt),
                self.metadata.style,
            )
            print("Generated description: ", description)

            print("Generating image...")
            images = self._generate_image(
                prompt,
                self.metadata.negative_prompt,
                self.metadata.model,
                self.metadata.size,
            )
            print("Generated image: ", len(images))
            image_filepath = f"/tmp/{self.metadata.model}_{i}_{uuid.uuid4().hex}.png"
            with open(image_filepath, "wb") as f:
                f.write(images[0])

            posts.append(Post(title=title, description=description, tags=[], publicity=PostPublicity.PUBLIC, content=image_filepath))
        
        return posts





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


