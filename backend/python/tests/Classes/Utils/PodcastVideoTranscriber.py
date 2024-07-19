import unittest
from src.Classes.Utils.PodcastTranscriber import PodcastTranscriber
from src.utils import format_yt_video_url
import os


class PodcastVideoTranscriber(unittest.TestCase):
    def setUp(self):
        test_podcast_url = os.environ.get("TEST_PODCAST_URL") or ""
        self.assembly_api_key = os.environ.get("ASSEMBLY_API_KEY") or ""

        if not test_podcast_url or not self.assembly_api_key:
            raise Exception("Test podcast url or assembly api key is empty string")

        self.podcast_url = format_yt_video_url(test_podcast_url)

    def test_api_key_exists(self):
        self.assertNotEqual(
            self.assembly_api_key, "", "AssemblyAI API key should not be empty"
        )

    def test_assembly_ai_transcription(self):
        transcriber = PodcastTranscriber.from_assembly(
            podcast_url=self.podcast_url, api_key=self.assembly_api_key, debugging=True
        )
        transcription = transcriber.transcript
        self.assertIsNotNone(transcription)

    def test_youtube_api_transcription(self):
        transcriber = PodcastTranscriber.from_transcription_api(
            podcast_url=self.podcast_url, debugging=True
        )
        transcription = transcriber.transcript
        self.assertIsNotNone(transcription)
