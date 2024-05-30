import unittest
from src.Classes import PodcastToShorts

class test_transcript(unittest.TestCase):

    def test_create_channel_success(self):
        podcastToShorts = PodcastToShorts(podcast_url="https://youtu.be/nDLb8_wgX50?si=d8jgLM_KO68OZHZI")
        # Test the create_channel function with valid inputs

        if result:
            print(result)
            # Assert that the channel was created successfully
            self.assertEqual(result["message"], "Channel created successfully")
            self.assertIsNotNone(result["channel_id"])
            self.assertIsNotNone(result["cookies"])
            self.assertIsNotNone(result["cookies"])
            self.assertIsNotNone(result["channel_name"])
            self.assertIsNotNone(result["channel_handle"])
        else:
            raise Exception("Channel creation failed, result is None")

