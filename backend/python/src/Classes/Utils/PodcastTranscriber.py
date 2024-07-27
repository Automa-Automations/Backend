import os
from typing import List, Tuple, Optional
from assemblyai.types import TranscriptResponse
from pydub import AudioSegment
import assemblyai as aai
import logging
import json
from aliases import PodcastTranscript
from models import (
    ParsedTranscript,
)
from src.utils import download_podcast

logger = logging.getLogger(__name__)


class PodcastTranscriber:
    """
    Class to transcribe a podcast
    """

    def __init__(self, debugging: Optional[bool] = False):
        self.debugging = debugging
        self.parsed_transcript_path = (
            "./src/Classes/Bots/json_files/assembly_parsed_transcript.json"
        )
        self.transcript_path = "./src/Classes/Bots/json_files/assembly_transcript.json"

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

    def get_transcript(
        self, podcast_url: str, api_key: str, debugging: bool = False
    ) -> Tuple[PodcastTranscript, float]:
        """
        Class method to create PodcastTranscriber object from AssemblyAI
        Parameters:
        - podcast_url: str: The url of the podcast
        - api_key: str: The AssemblyAI API key
        - debugging: bool: The debugging flag
        Returns Union['PodcastTranscriber', None] - The instantiated PodcastTranscriber object. Returns none if transcription failed.

        """
        aai.settings.api_key = api_key
        download_output = download_podcast(podcast_url)
        logger.info(f"Download Output: {download_output}")
        download_path = os.path.join(
            download_output.output_path, download_output.filename
        )

        test_podcast_mp3_path = download_path.rsplit(".", 1)[0] + ".mp3"
        if debugging and os.path.exists(test_podcast_mp3_path):
            logger.info(
                f"Mp3 file already exist, no need to convert video to mp3. Path: {test_podcast_mp3_path}"
            )
            podcast_mp3_path = test_podcast_mp3_path
        else:
            podcast_mp3_path = self._convert_to_mp3(download_path)

        if (
            debugging
            and os.path.exists(self.parsed_transcript_path)
            and os.path.exists(self.transcript_path)
        ):
            logger.info("Transcript already exist, no need to transcribe podcast.")
            with open(self.parsed_transcript_path, "r") as f:
                parsed_transcript: List[ParsedTranscript] = json.load(f)
            with open(self.transcript_path, "r") as f:
                transcript: TranscriptResponse = json.load(f)
        else:
            transcript = self._get_yt_podcast_transcription(podcast_mp3_path)
            parsed_transcript = self._parse_transcript(transcript)

        if not transcript:
            raise Exception("Transcription failed.")
        else:
            audio_duration = transcript.audio_duration
            if not audio_duration:
                raise Exception("Transcription failed. Audio duration is None.")

        return (parsed_transcript, audio_duration)

    def _get_yt_podcast_transcription(
        self, podcast_download_path: str
    ) -> TranscriptResponse:
        """
        Function to transcribe the podcast, using Assembly AI
        Parameters:
        - podcast_download_path: str: The path to the downloaded podcast
        Returns Union[TranscriptResponse] - The transcript of the podcast
        """
        logger.info("Transcribing podcast...")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(podcast_download_path)
        transcript = transcript.wait_for_completion()
        if transcript.json_response:
            if "text" in transcript.json_response:
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
                raise Exception(
                    f"Transcription failed! It doesn't have 'text' as a key. Transcript: {transcript.json_response}"
                )
        else:
            raise Exception(f"Transcription failed! 'json_response' is None.")

    def _parse_transcript(self, transcript) -> List[ParsedTranscript]:
        """Function to parse transcript into full sentences."""
        logger.info("Parsing transcript...")

        current_sentence_dict = ParsedTranscript(
            sentence="", start_time=0, end_time=0, speaker=""
        )

        full_sentences_transcript: List[ParsedTranscript] = []
        for word_dict in transcript["words"]:
            current_sentence_dict.sentence += word_dict["text"] + " "
            if word_dict["text"][0].isupper() and not current_sentence_dict.start_time:
                current_sentence_dict.start_time = word_dict["start"]
                current_sentence_dict.speaker = word_dict["speaker"]

            if current_sentence_dict.sentence.strip()[-1] in [
                "?",
                "!",
                ".",
            ]:
                current_sentence_dict.end_time = word_dict["end"]
                current_sentence_dict.sentence = current_sentence_dict.sentence.strip()
                full_sentences_transcript.append(current_sentence_dict)
                current_sentence_dict = ParsedTranscript(
                    sentence="",
                    start_time=0,
                    end_time=0,
                    speaker="",
                )

        logger.info(
            f"Full sentences transcript length: {len(full_sentences_transcript)}"
        )
        if self.debugging:
            with open(self.parsed_transcript_path, "w") as f:
                f.write(json.dumps(full_sentences_transcript, indent=4))

        logger.info("Transcription parsing complete.")
        return full_sentences_transcript
