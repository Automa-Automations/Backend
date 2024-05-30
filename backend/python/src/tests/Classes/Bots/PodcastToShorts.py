import unittest
from  src.Classes.Bots import PodcastToShorts

class FullRun(unittest.TestCase):
    def full_run(self):
        podcast_to_shorts = PodcastToShorts(podcast_url="https://youtu.be/nDLb8_wgX50?si=d8jgLM_KO68OZHZI")
        shorts = podcast_to_shorts.get_shorts()

        self.assertEqual(isinstance(shorts, list), True)
        self.assertIsNotNone(shorts[0])
        self.assertEqual(isinstance(shorts[0], dict), True)

class ClipShorts(unittest.TestCase):
    podcast_to_shorts = PodcastToShorts(podcast_url="https://youtu.be/nDLb8_wgX50?si=d8jgLM_KO68OZHZI")

    def clip_shorts(self):
        return

def download_video():
    return

def get_video_transcript():
    return
