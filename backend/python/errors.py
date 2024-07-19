import json
from aliases import VideoType, VideoEditingActionType


class DownloadError(Exception):
    """
    Custom error class for any error related to downloading something
    """

    def __init__(self, message: str, download_type: str):
        """
        Parameters:
        - message: str: The error message you
        - download_type: str: The type of download that was attempted
        """
        message = json.dumps(
            {
                "error_type": "Download Error",
                "info": message,
                "download_type": download_type,
            },
            indent=4,
        )
        super().__init__(message)


class EditVideoError(Exception):
    """
    Custom error class for any error related to editing a video
    """

    def __init__(
        self,
        message: str,
        video_type: VideoType,
        action_type: VideoEditingActionType,
    ) -> None:
        """
        Parameters:
        - message: str: The error message you want to show
        - video_type: VideoType: The type of video (short, long form for example)
        - action_type: VideoEditingActionType: The type of editing/action that was attempted
        """
        message = json.dumps(
            {
                "error_type": "Video Edit Error",
                "info": message,
                "video_type": video_type,
                "action_type": action_type,
            },
            indent=4,
        )
        super().__init__(message)
