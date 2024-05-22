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
    llama_model: str = "llama3"
    system_prompt: str = f"""
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
        full_sentences_transcript = self.__get_full_sentences_transcript()
        transcriptions_feedback = self.__get_transcripts_feedback(full_sentences_transcript)
        shorts_transcripts = self.__filter_transcripts(transcriptions_feedback)

    def __filter_transcripts(self, transcriptions_feedback, should_make_short = True):
        """
        Method to filter the transcriptions based on the should_make_short value
        Parameters:
        - transcriptions_feedback: list: The list of the feedback of the transcriptions
        - should_make_short: bool: The value to filter the transcriptions
        Returns:
        - list: The list of the transcriptions that have the should_make_short value
        """
        return [transcription for transcription in transcriptions_feedback if transcription["stats"]["should_make_short"] == should_make_short]

    def __get_transcripts_feedback(self, full_sentences_transcript): 
        chunked_transcript = self.__chunk_transcript(full_sentences_transcript)
        system_prompt = f"""
        You take in a transcript, and you decide whether or not the transcript is valid for a short. You also evaluate the short based off of this:
        score: a score out of a 100, on how good this would make for a short. 
        should_make_short: True or False. True, if the score is above or equal to 70, false if it is below 70
        feedback: Any feedback you have on the short, what is good and bad about the transcript, how to make it better.
        ###
        Here is a few example outputs you might give, you respond in JSON (ignore the values, this is just so that you know the exact output structure):
            {
                "score": 65,
                "should_make_short": False,
                "feedback": "The transcript is too long, and the content is not engaging enough.",
            }
        """
        message = f"Here is the transcript: {full_sentences_transcript}" 

        transcripts_feedback = []
        for chunk in chunked_transcript:
            response = client.generate(
                model=self.llama_model,
                system=system_prompt,
                prompt=message,
                format="json",
            )["response"]
            if response["score"] >= 80 and response["should_make_short"] == True:
                highlight = {
                    "transcript": chunk,
                    "stats": response
                }
                transcripts_feedback.append(highlight)
        return transcripts_feedback

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

    def __chunk_transcript(self, video_transcript: str, chunk_length: int = 2000):
        # chunk the list of dictionaries into a final list of lists, each list having less than chunk_length amount of characters
        chunk_transcript_list = []
        for i in range(0, len(video_transcript), chunk_length):
            chunk_transcript_list.append(video_transcript[i:i + chunk_length])

        return chunk_transcript_list

    def __get_full_sentences_transcript(self):
        video_transcript = self.__get_video_transcript(self.podcast_url)
        chunked_transcript = self.__chunk_transcript(video_transcript)

        full_sentences_transcript = []
        for chunk in chunked_transcript:
            chunk_transcript  = self.__format_full_sentences_transcript(chunk, self.system_prompt)
            full_sentences_transcript.extend(chunk_transcript)

        return full_sentences_transcript

    def __validate_env_variables(self):
        if not OLLAMA_HOST_URL:
            raise ValueError("OLLAMA_HOST_URL is not set in the environment variables")
