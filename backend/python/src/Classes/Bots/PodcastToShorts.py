from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List 
from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_HOST_URL=os.getenv("OLLAMA_HOST_URL")

# import dataclass
from dataclasses import dataclass

client = Client(OLLAMA_HOST_URL)

@dataclass
class PodcastToShorts:
    podcast_url: str
    prompt: Optional[str] = None
    llama_model: str = "llama3"
    system_prompt: Optional[str] = f"""
    You take in a transcirpt from a video, and merge the dictionaries into less dictionaries, by making full sentences. Here is an example:
    ###
    Input: [{'start': 0.0, 'duration': 2.0, 'text': 'Hello'}, {'start': 2.0, 'duration': 2.0, 'text': 'world!'}]
    Output: [{'start': 0.0, 'duration': 4.0, 'text': 'Hello world!'}]

    You always output in json format.
    """

    def __post_init__(self):
        self.__validate_env_variables()

    def get_shorts(self):
        """
        Method to generate the shorts from the podcast
        """

        video_transcript = self.__get_video_transcript(self.podcast_url)
        chunked_transcript = self.__chunk_transcript()
        video_transcript_sentences = self.__format_full_sentences_transcript(video_transcript, self.system_prompt)

    def __get_video_transcript(self, video_url: str):
        """
        Method to get the video transcript from the video url
        Parameters:
        - video_url: str: The url of the video
        Returns:
        - video_transcript: list: The list of the transcript of the video
        """
        if "youtu.be" in video_url:
            # Share url type
            video_id = video_url.split("?")[0].split("be/")[1]
            print(f"Video ID: {video_id}")
        elif "youtube" in video_url:
            # watch url type
            video_id = video_url.split("v=")[1]
            print(f"Video ID: {video_id}")
        else:
            raise ValueError(f"Incorrect url format: {video_url}")

        video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return video_transcript

    def __format_full_sentences_transcript(self, transcript: List[dict], system_prompt: str):
        message = f"Here is the transcript: {transcript}" 
        return client.generate(
            model=self.llama_model,
            system=system_prompt,
            prompt=message,
            format="json",
        )["response"]

    def __validate_env_variables(self):
        if not OLLAMA_HOST_URL:
            raise ValueError("OLLAMA_HOST_URL is not set in the environment variables")
