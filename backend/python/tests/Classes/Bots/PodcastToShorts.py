import unittest
from src.Classes.Bots import PodcastToShorts

podcast_url = "https://youtu.be/nDLb8_wgX50?si=d8jgLM_KO68OZHZI"

class FullRun(unittest.TestCase):
    def test_full_run(self):
        self.assertEqual(True, True)
        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        shorts = podcast_to_shorts.get_shorts()

        self.assertEqual(isinstance(shorts, list), True)
        self.assertIsNotNone(shorts[0])
        self.assertEqual(isinstance(shorts[0], dict), True)

class ClipShorts(unittest.TestCase):
    def test_clip_shorts(self):
        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        # skip this test since clipping functionality isn't made yet.
        self.assertEqual(True, True)


class DownloadVideo(unittest.TestCase):
    def test_download_video(self):
        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        output = podcast_to_shorts._download_podcast("")

        self.assertEqual(isinstance(output["output_path"], str), True)
        self.assertEqual(isinstance(output["filename"], str), True)
        self.assertEqual(output["status"], "success")


class GetFullTranscript(unittest.TestCase):
    def test_get_full_transcript(self):
        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        transcript = podcast_to_shorts._get_video_transcript(podcast_url)
        print(f"transcript: {transcript}")

        self.assertEqual(isinstance(transcript, list), True)
        self.assertEqual(isinstance(transcript[0], dict), True)
        self.assertEqual(isinstance(transcript[0]["text"], str), True)
        self.assertEqual(isinstance(transcript[0]["start"], float), True)
        self.assertEqual(isinstance(transcript[0]["duration"], float), True)
