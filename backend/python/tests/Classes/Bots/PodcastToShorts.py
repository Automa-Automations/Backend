import unittest
from moviepy.editor import VideoFileClip
from src.Classes.Bots import PodcastToShorts
from typing import Literal
import os
import logging

logger = logging.getLogger(__name__)

env_type = "LOCAL_"
if os.environ.get("CURRENT_ENVIRONMENT", "local") == "prod":
    env_type = "HOSTED_"

assembly_api_key = os.environ.get("ASSEMBLY_API_KEY") or ""
llm_api_key = os.environ.get("OPENAI_API_KEY") or ""

podcast_url = os.environ.get("TEST_PODCAST_URL") or ""
transcriptor_type: Literal["assembly_ai", "yt_transcript_api"] = "assembly_ai"
llm_model = os.environ.get("LLM_TESTING_MODEL") or ""


class FullRun(unittest.TestCase):
    def test_full_run(self):
        self.assertEqual(True, True)
        podcast_to_shorts = PodcastToShorts(
            podcast_url=podcast_url,
            llm_type=llm_type,
            llm_model=llm_model,
            transcriptor_type=transcriptor_type,
        )
        podcast_to_shorts.llm_api_key = llm_api_key

        if transcriptor_type == "assembly_ai":
            podcast_to_shorts.assembly_api_key = assembly_api_key

        podcast_to_shorts.assembly_api_key = assembly_api_key
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
