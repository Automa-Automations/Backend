import json
from src.Classes.Bots import PodcastToShorts


def handler(event, context):
    try:
        body = json.loads(event["body"])
        podcast_url = body["podcast_url"]

        podcast_to_shorts = PodcastToShorts(podcast_url=podcast_url)
        shorts_result = podcast_to_shorts.get_shorts()

        return {
            "statusCode": 200,
            "body": json.dumps(shorts_result),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": e}),
        }
