from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List 
from ollama import Client
from dotenv import load_dotenv
from pytube import YouTube
import os
import json

load_dotenv()

OLLAMA_HOST_URL=os.getenv("OLLAMA_HOST_URL")

# import dataclass
from dataclasses import dataclass

llama_client = Client(OLLAMA_HOST_URL)

@dataclass
class PodcastToShorts:
    podcast_url: str
    llama_model: str = "llama3"

    def __post_init__(self):
        self.__validate_env_variables()
        self.yt = YouTube(self.podcast_url)

    def get_shorts(self):
        """
        Method to generate the shorts from the podcast
        """
        full_sentences_transcript = self.__get_full_sentences_transcript()
        print(f"Full Sentences Transcript: (length: {len(full_sentences_transcript)}): {full_sentences_transcript}")

        transcriptions_feedback = self.__get_transcripts_feedback(full_sentences_transcript)
        print(f"Transcriptions With Feedback: (length: {len(transcriptions_feedback)}): {transcriptions_feedback}")

        shorts_transcripts = self.__filter_transcripts(transcriptions_feedback)
        print(f"Shorts Transcripts: (length: {len(shorts_transcripts)}): {shorts_transcripts}")

        # take each short, use OpenAI to remove all unnecessary content in the start, middle and end, so that it is just the short. 
        shorts_final_transcripts = self.__get_shorts_final_transcripts(shorts_transcripts)
        print(f"Shorts Final Transcripts: (length: {len(shorts_final_transcripts)}): {shorts_final_transcripts}")

        clip_shorts_data = self._generate_shorts(shorts_transcripts, shorts_final_transcripts)
        print(f"Clip Shorts Data: (length: {len(clip_shorts_data)}): {clip_shorts_data}")

        return clip_shorts_data

    def __get_shorts_final_transcripts(self, shorts_transcripts: List[dict]):
        """
        Method to get the final transcripts of the shorts, by removing the start and end sentences, to get the optimized short.
        Parameters:
        - shorts_transcripts: list: The list of the shorts transcripts
        Returns: 
        - list: The list of the final transcripts of the shorts
        """
        system_prompt = f"""
        You get in a transcript, and you are supposed to remove sentences dictionaries in the transcript, so that the transcript only have the part that will be fitting for a short. Make it 100 - 150 words max, and take in the total length into account, as the total length of all sentences dictionaries combined may be at max 55 seconds. The final clip should be in a great format for a social media short, so the primary goal is to make the short get as much views as possible. Here is an example input and output formats:
        ###
        Input (the input will be provided to you by the user): 
        {json.dumps({
            "transcript": [{'start': 0.0, 'duration': 2.0, 'text': 'sentence 1 text here'}, "..."],
            "stats": {
                "score": 65,
                "should_make_short": False,
                "feedback": "The transcript is too long, and the content is not engaging enough."
            }
        }, indent=4)}
        Output (you give the output, in this exact format. Make sure to put the transcript in the "transcript" list): 
        {json.dumps({
            "transcript": [{'start': 0.0, 'duration': 2.0, 'text': 'Hello world!'}], # Change the transcription, to be fitting for a short that will be optimized for the most amount of views. 
        }, indent=4)}
        """
        final_transcripts = []
        for short in shorts_transcripts:
            message = f"Here is the transcript: {json.dumps(short, indent=4)}"
            llama_response = llama_client.generate(
                model=self.llama_model,
                system=system_prompt,
                prompt=message,
                format="json",
            )["response"]

            append_dict = {
                "transcript": json.loads(llama_response)["transcript"],
                "stats": short["stats"]
            }
            final_transcripts.append(append_dict)

        return final_transcripts

    def _generate_shorts(self, shorts_transcripts: List[dict], shorts_final_transcripts: List):
        # for now, just download the podcast and get shorts, unedited.
        download_response = self.__download_podcast();
        if download_response["status"] == "success":
            clip_shorts_data = []
            for short in shorts_final_transcripts:
                clipped_short_data = self._clip_short(short, download_response["output_path"], download_response["filename"], short)
                clip_shorts_data.append(clipped_short_data)

            return clip_shorts_data
        else:
            raise ValueError(f"Error while downloading the podcast: {download_response['error']}")

    def _clip_short(self, short: dict, output_path: str, filename: str, short_transcript):
        print("Clipping short")
        print(short)
        return

    def __download_podcast(self, output_path: str = "downloads/", filename: str = ""):
        try:
            if filename == "":
                filename = self.yt.title

            self.yt.streams.get_highest_resolution().download(output_path=output_path, filename=filename)
            return {
                "output_path": output_path, 
                "filename": filename, 
                "status": "success",
            }
        except Exception as e:
            return {
                "error": e,
                "status": "error",
            }

    def __filter_transcripts(self, transcriptions_feedback: List[dict], should_make_short : bool = True):
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
        """
        Method to get the feedback of the transcriptions
        Parameters:
        - full_sentences_transcript: list: The list of the full sentences of the transcriptions
        Returns: 
        - list: The list of the feedback of the transcriptions
        """
        chunked_transcript = self.__chunk_transcript(full_sentences_transcript)
        system_prompt = f"""
        You take in a transcript, and you decide whether or not the transcript is valid for a short. You also evaluate the short based off of this:
        score: a score out of a 100, on how good this would make for a short. 
        should_make_short: True or False. True, if the score is above or equal to 70, false if it is below 70
        feedback: Any feedback you have on the short, what is good and bad about the transcript, how to make it better.
        ###
        Here is a few example outputs you might give, you respond in JSON (ignore the values, this is just so that you know the exact output structure):
            {json.dumps({
                "score": 65,
                "should_make_short": False,
                "feedback": "The transcript is too long, and the content is not engaging enough.",
            }, indent=4)}
        """
        message = f"Here is the transcript: {full_sentences_transcript}" 

        transcripts_feedback = []
        for chunk in chunked_transcript:
            response = llama_client.generate(
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
        """
        Method to format the full sentences transcript
        Parameters:
        - transcript: List[dict]: The list of the transcript
        - system_prompt: str: The system prompt
        Returns:
        - list: The list of the formatted transcript
        """
        message = f"Here is the transcript: {transcript}" 
        llama_response = llama_client.generate(
            model=self.llama_model,
            system=system_prompt,
            prompt=message,
            format="json",
        )["response"]

        return json.loads(llama_response)["transcript"]

    def __chunk_transcript(self, video_transcript: str, chunk_length: int = 2000):
        """
        Method to chunk the transcript
        Parameters:
        - video_transcript: str: The video transcript
        - chunk_length: int: The length of the chunk
        Returns:
        - list: The list of the chunked transcript
        """
        # chunk the list of dictionaries into a final list of lists, each list having less than chunk_length amount of characters
        chunk_transcript_list = []
        for i in range(0, len(video_transcript), chunk_length):
            chunked_transcript = video_transcript[i:i + chunk_length]
            print(f"\n\n{i+1}. Chunked Transcript (length: {len(chunked_transcript)}): {chunked_transcript}")
            with open("chunk_transcript.json", "w") as f:
                f.write(json.dumps(chunked_transcript, indent=4))
                print(f"(length: {len(chunked_transcript)}) Saved chunk transcript to 'chunk_transcript.json'")

            chunk_transcript_list.append(chunked_transcript)

        return chunk_transcript_list

    def __get_full_sentences_transcript(self):
        """
        Method to get the full sentences transcript
        Returns:
        - list: The list of the full sentences transcript
        """
        video_transcript = self.__get_video_transcript(self.podcast_url)
        print(f"Video Transcript (length: {video_transcript}): {video_transcript}")

        chunked_transcript = self.__chunk_transcript(video_transcript)

        system_prompt = f"""
        You are a assistant, where you will be given a messy transcription list. Your job is to format the transcript, so that it is in a good format for a short, by forming full sentences. Here an simplified input you might get, along with the output format: 
        {json.dumps({"transcripts": [{'start': 0.0, 'duration': 4.0, 'text': 'hello there'}, {'start': 5.2, 'duration': 4.0, 'text': 'I am bob'}, {'start': 9.6, 'duration': 5.0, 'text': 'i love building cool stuff'}]}, indent=4)}
        ###
        Your job is to take the input the user have given you, and format all the objects into great formats: {json.dumps({"transcripts": [{'start': 0.0, 'duration': 14.6, 'text': 'Hello there! I am Bob, and I love building cool stuff.'}]}, indent=4)}
        ###
        As you can see, the way it calculated the duration is by looking at the last sentence part, the one with the text "i love building cool stuff", taking the "start" and "end" duration, and adding them together, toget the duration of 14.6. Make sure the "start" and "duration" is entirely correct, this is really important.
        """
        full_sentences_transcript = []
        for chunk in chunked_transcript:
            chunk_transcript  = self.__format_full_sentences_transcript(chunk, system_prompt)
            full_sentences_transcript.extend(chunk_transcript["transcripts"])

        return full_sentences_transcript

    def __validate_env_variables(self):
        """
        Method to evaluate the environment variables, and raise error if needed 
        """
        if not OLLAMA_HOST_URL:
            raise ValueError("OLLAMA_HOST_URL is not set in the environment variables")
