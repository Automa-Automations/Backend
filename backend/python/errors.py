import json


class DownloadError(Exception):
    def __init__(self, message: str, download_type: str):
        message = json.dumps(
            {
                "error_type": "Download Error",
                "info": message,
                "download_type": download_type,
            },
            indent=4,
        )
        super().__init__(message)
