import os
from typing import List, Union
from assemblyai.types import TranscriptResponse
from youtube_transcript_api import YouTubeTranscriptApi
from pydub import AudioSegment
import assemblyai as aai
import logging
import json
from models import AssemblyAIParsedTranscriptType, YoutubeAPITranscript
from src.utils import download_podcast

logger = logging.getLogger(__name__)


class PodcastTranscriber:
    """
    Class to transcribe a podcast
    """

    def __init__(self, podcast_url) -> None:
        self.podcast_url = podcast_url
        self.aai_transcript: List[AssemblyAIParsedTranscriptType] = []
        self.yt_transcript: List[YoutubeAPITranscript] = []
        self.audio_duration = 0

    def _convert_to_mp3(self, file_path: str) -> str:
        """
        Function to convert mp4 file to mp3 file
        Parameters:
        - file_path: str: The path to the mp4 file
        Returns str - The path to the mp3 file
        """
        logger.info(f"Converting {file_path} to mp3")
        mp4_audio = AudioSegment.from_file(file_path, format="mp4")
        mp3_file_path = ".".join(file_path.split(".")[:-1]) + ".mp3"
        mp4_audio.export(mp3_file_path, format="mp3")
        return mp3_file_path

    @classmethod
    def from_assembly(
        cls, podcast_url: str, api_key: str, debugging: bool = False
    ) -> Union["PodcastTranscriber", None]:
        """
        Class method to create PodcastTranscriber object from AssemblyAI
        Parameters:
        - podcast_url: str: The url of the podcast
        - api_key: str: The AssemblyAI API key
        - debugging: bool: The debugging flag
        Returns Union['PodcastTranscriber', None] - The instantiated PodcastTranscriber object. Returns none if transcription failed.
        """
        podcast_transcriber = cls(podcast_url)
        download_output = download_podcast(podcast_url)
        logger.info(f"Download Output: {download_output}")

        if download_output["status"] == "success":
            download_path = os.path.join(
                download_output["output_path"], download_output["filename"]
            )

            assembly_ai = AssemblyAI(api_key)
            assembly_ai.debugging = debugging

            test_podcast_mp3_path = download_path.rsplit(".", 1)[0] + ".mp3"
            if debugging and os.path.exists(test_podcast_mp3_path):
                logger.info(
                    f"Mp3 file already exist, no need to convert video to mp3. Path: {test_podcast_mp3_path}"
                )
                podcast_mp3_path = test_podcast_mp3_path
            else:
                podcast_mp3_path = podcast_transcriber._convert_to_mp3(download_path)

            if (
                debugging
                and os.path.exists(assembly_ai.parsed_transcript_path)
                and os.path.exists(assembly_ai.transcript_path)
            ):
                logger.info("Transcript already exist, no need to transcribe podcast.")
                with open(assembly_ai.parsed_transcript_path, "r") as f:
                    parsed_transcript: List[AssemblyAIParsedTranscriptType] = json.load(
                        f
                    )
                with open(assembly_ai.transcript_path, "r") as f:
                    transcript = json.load(f)
            else:
                transcript = assembly_ai.get_yt_podcast_transcription(podcast_mp3_path)
                parsed_transcript = assembly_ai.parse_transcript(transcript)

            podcast_transcriber.aai_transcript = parsed_transcript
            if not transcript:
                raise Exception("Transcription failed.")
            else:
                podcast_transcriber.audio_duration = transcript["audio_duration"]
        return podcast_transcriber

    @classmethod
    def from_transcription_api(
        cls, podcast_url: str, debugging: bool = False
    ) -> "PodcastTranscriber":
        """
        Class method to create PodcastTranscriber object from YoutubeTranscriptionAPI
        Parameters:
        - podcast_url: str: The url of the podcast
        - debugging: bool: The debugging flag
        Returns PodcastTranscriber - The instantiated PodcastTranscriber object
        """
        podcast_transcriber = cls(podcast_url)
        transcription_api = YoutubeTranscriptionAPITranscriber(podcast_url)
        transcription_api.debugging = debugging
        podcast_transcriber.yt_transcript = transcription_api.get_video_transcript()
        return podcast_transcriber


class AssemblyAI:
    """
    Class to interact with AssemblyAI API, specifically for transcriptions
    """

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        aai.settings.api_key = api_key
        self.debugging = False
        self.parsed_transcript_path = (
            "./src/Classes/Bots/json_files/assembly_parsed_transcript.json"
        )
        self.transcript_path = "./src/Classes/Bots/json_files/assembly_transcript.json"

    def get_yt_podcast_transcription(
        self, podcast_download_path: str
    ) -> Union[TranscriptResponse, None]:
        """
        Function to transcribe the podcast, using Youtube Transcript API
        Parameters:
        - podcast_download_path: str: The path to the downloaded podcast
        Returns Union[TranscriptResponse, None] - The transcript of the podcast
        """
        logger.info("Transcribing podcast...")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(podcast_download_path)
        transcript = transcript.wait_for_completion()
        if transcript.json_response and "text" in transcript.json_response:
            logger.info(
                f"Transcript word length: {len(transcript.json_response["text"])}"
            )

            if self.debugging:
                with open(self.transcript_path, "w") as f:
                    f.write(json.dumps(transcript.json_response, indent=4))

            transcript_response: TranscriptResponse = json.loads(
                json.dumps(transcript.json_response)
            )
            return transcript_response
        else:
            logger.error("Transcription failed.")

    def parse_transcript(self, transcript) -> List[AssemblyAIParsedTranscriptType]:
        """Function to parse transcript into full sentences."""
        logger.info("Parsing transcript...")
        all_transcript_words = self.remove_filler_words(transcript["words"])

        full_sentences_transcript: List[AssemblyAIParsedTranscriptType] = []
        current_sentence_dict: AssemblyAIParsedTranscriptType = {
            "sentence": "",
            "start_time": 0,
            "end_time": 0,
            "speaker": "",
        }

        for word_dict in all_transcript_words:
            current_sentence_dict["sentence"] += word_dict["text"] + " "
            if (
                word_dict["text"][0].isupper()
                and not current_sentence_dict["start_time"]
            ):
                current_sentence_dict["start_time"] = word_dict["start"]
                current_sentence_dict["speaker"] = word_dict["speaker"]

            if current_sentence_dict["sentence"].strip()[-1] in [
                "?",
                "!",
                ".",
            ]:
                current_sentence_dict["end_time"] = word_dict["end"]
                current_sentence_dict["sentence"] = current_sentence_dict[
                    "sentence"
                ].strip()
                full_sentences_transcript.append(current_sentence_dict)
                current_sentence_dict = {
                    "sentence": "",
                    "start_time": 0,
                    "end_time": 0,
                    "speaker": "",
                }

        logger.info(
            f"Full sentences transcript length: {len(full_sentences_transcript)}"
        )
        if self.debugging:
            with open(self.parsed_transcript_path, "w") as f:
                f.write(json.dumps(full_sentences_transcript, indent=4))

        logger.info("Transcription parsing complete.")
        return full_sentences_transcript

    def remove_filler_words(self, word_dicts_array: List[aai.Word]) -> List[aai.Word]:
        """
        Function to remove filler words from the transcript
        Parameters:
        - word_dicts_array: List[aai.Word]: The array of word dictionaries
        Returns List[aai.Word] - The array of word dictionaries with filler words removed
        """
        filler_words = [
            "um",
            "uh",
            "ah",
            "literally",
            "uh-huh",
            "oh",
            "uh-oh",
            "hmm",
        ]
        final_word_dicts_array: List[aai.Word] = []
        for word_dict in word_dicts_array:
            if word_dict["text"] not in filler_words:
                final_word_dicts_array.append(word_dict)

        return final_word_dicts_array


class YoutubeTranscriptionAPITranscriber:
    """
    Class to interact with Youtube API to get the transcript of a Youtube video
    """

    def __init__(self, podcast_url: str) -> None:
        self.podcast_url = podcast_url
        self.debugging = False
        self.transcript_path = "./src/Classes/Bots/json_files/youtube_transcript.json"

    def get_video_transcript(self) -> List[YoutubeAPITranscript]:
        """
        Method to get the video transcript from the video url
        Returns List[YoutubeAPITranscriptDict] - The transcript of the podcast
        """
        logger.info("Getting video transcript...")
        video_id = self.podcast_url.split("v=")[1]
        video_transcript: List[YoutubeAPITranscript] = json.loads(
            json.dumps(YouTubeTranscriptApi.get_transcript(video_id))
        )

        with open(self.transcript_path, "w") as f:
            f.write(json.dumps(video_transcript, indent=4))

        return video_transcript
