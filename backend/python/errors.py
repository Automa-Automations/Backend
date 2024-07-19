import json
from aliases import VideoType, VideoEditingActionType


class DownloadError(Exception):
    """
    Exception raised related to downloading something
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
    Exception raised related to editing a video
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


class ImpossibleError(Exception):
    """Exception raised for code paths that should be impossible"""

    def __init__(self, message: str, explanation: str):
        """
        Parameters:
        - message: str: The error message you want to show
        - explanation: str: The explanation of why this error should be impossible
        """
        message = json.dumps(
            {
                "error_type": "Impossible Error",
                "explanation": explanation,
                "message": message,
            },
            indent=4,
        )
