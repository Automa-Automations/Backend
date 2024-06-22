import unittest
from moviepy.editor import VideoFileClip
from src.Classes.Bots import PodcastToShorts
import os
import logging

logger = logging.getLogger(__name__)

podcast_url = os.environ.get("TEST_PODCAST_URL") or ""

class FullRun(unittest.TestCase):
    def test_full_run(self):
        self.assertEqual(True, True)
        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        shorts = podcast_to_shorts.get_shorts()

        self.assertEqual(isinstance(shorts, list), True)
        self.assertIsNotNone(shorts[0])
        self.assertEqual(isinstance(shorts[0], dict), True)

class ClipAndFollowFacesMobileRatio(unittest.TestCase):
    def test_clip_and_follow_faces_mobile_ratio(self):
        test_clip_path = "test_assets/test_clip.mp4"
        test_clipped_video = VideoFileClip(test_clip_path)
        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        clipped_video_response = podcast_to_shorts._clip_and_follow_faces_mobile_ratio(
            test_clipped_video
        )

        self.assertTrue("error" not in clipped_video_response)
        self.assertTrue("short_transcript" in clipped_video_response)
