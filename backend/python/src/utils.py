import sys
from errors import DownloadError
from src.supabase import supabase
from typing import Any, Optional
from pytube import YouTube
import datetime
import traceback
import uuid
import requests
from fuzzywuzzy import fuzz
import os
from models import DownloadPodcastResponse
from aliases import ReturnStatus
import logging

logger = logging.getLogger(__name__)


def update_value(
    table: str, line: str, val: str, new_value: Any, line_name: str = "id"
):
    try:
        if isinstance(new_value, datetime.datetime):
            new_value = str(new_value)

        supabase.table(table).update({val: new_value}).eq(line_name, line).execute()
    except Exception as e:
        print(e, traceback.format_exc())


def get_value(table: str, line: Any, line_name: str = "id") -> dict:
    try:
        return supabase.table(table).select("*").eq(line_name, line).execute().data[0]
    except Exception as e:
        print(e, traceback.format_exc())
    return {}


def upload_file(
    bucket_name: str,
    path_on_bucket: str,
    content: bytes,
    extended_file_options=None,
) -> str:
    if extended_file_options is None:
        extended_file_options = {}

    new_file_name = uuid.uuid4()
    file_path_segments = path_on_bucket.split("/")
    filename, extension = file_path_segments[-1].split(".")
    filename = f"{new_file_name}_{filename}_{datetime.datetime.now().timestamp()}"
    full_filename = f"{filename}.{extension}"
    joined_file_segments = "/".join(file_path_segments)
    if len(joined_file_segments.split("/")) == 1:
        full_file_path = full_filename
    else:
        full_file_path = f"{joined_file_segments}/{full_filename}"

    file_options = {}
    match extension:
        # Image MIME Types
        case "png":
            file_options = {"content-type": "image/png"}
        case "jpg":
            file_options = {"content-type": "image/jpeg"}
        case "jpeg":
            file_options = {"content-type": "image/jpeg"}
        case "gif":
            file_options = {"content-type": "image/gif"}
        case "bmp":
            file_options = {"content-type": "image/bmp"}
        case "tiff":
            file_options = {"content-type": "image/tiff"}
        case "webp":
            file_options = {"content-type": "image/webp"}
        case "svg":
            file_options = {"content-type": "image/svg+xml"}

        # Audio MIME Types
        case "mp3":
            file_options = {"content-type": "audio/mpeg"}
        case "wav":
            file_options = {"content-type": "audio/wav"}
        case "ogg":
            file_options = {"content-type": "audio/ogg"}
        case "flac":
            file_options = {"content-type": "audio/flac"}
        case "aac":
            file_options = {"content-type": "audio/aac"}

        # Video MIME Types
        case "mp4":
            file_options = {"content-type": "video/mp4"}
        case "avi":
            file_options = {"content-type": "video/x-msvideo"}
        case "mov":
            file_options = {"content-type": "video/quicktime"}
        case "mkv":
            file_options = {"content-type": "video/x-matroska"}
        case "wmv":
            file_options = {"content-type": "video/x-ms-wmv"}

        # Text MIME Types
        case "txt":
            file_options = {"content-type": "text/plain"}
        case "html":
            file_options = {"content-type": "text/html"}
        case "css":
            file_options = {"content-type": "text/css"}
        case "csv":
            file_options = {"content-type": "text/csv"}
        case "xml":
            file_options = {"content-type": "text/xml"}
        case "json":
            file_options = {"content-type": "application/json"}
        case "pdf":
            file_options = {"content-type": "application/pdf"}
        case "doc":
            file_options = {"content-type": "application/msword"}
        case "docx":
            file_options = {
                "content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }

    # TODO: Recursively create the folder if it doesn't exist.
    # TODO: Create the bucket if it doesn't exist (With full rls lockdown always, because we don't want user interacting with the buckets at all!)
    # We want that type of functionality because it will allow us to easily bootstrap an entire project.
    supabase.storage.from_(bucket_name).upload(
        file=content,
        path=full_file_path,
        file_options={**file_options, **extended_file_options},
    )
    # res = supabase.storage.from_(bucket_name).get_public_url(full_file_path)
    res = supabase.storage.from_(bucket_name).create_signed_url(
        full_file_path, sys.maxsize
    )["signedURL"]
    return res


def download_file_url(from_: str) -> bytes:
    response = requests.get(from_)
    response_bytes = response.content
    file_object = response_bytes

    return file_object


def format_yt_video_url(video_url: str) -> str:
    """
    Function to format a Youtube video URL into a standard format
    Parameters:
    - video_url: str: The video URL
    Returns str: The formatted video URL
    """
    if "youtu.be" in video_url:
        video_url = f"https://youtube.com/watch?v={video_url.split("youtu.be/")[1].split("?")[0]}"

    return video_url


def download_podcast(
    podcast_url: str,
    output_path: str = "downloads/",
    filename: str = "",
    debugging: Optional[bool] = False,
) -> DownloadPodcastResponse:
    """
    Function to download a specific podcast
    Parameters:
    - podcast_url: str: The podcast URL
    - output_path: str: The output directory where you want to save the downloaded podcast
    - filename: str: The filename of the downloaded podcast
    - debugging: bool: Whether to print debugging information, along with skipping the download entirely if it already exists.
    Returns DownloadPodcastResponse: the download response
    """
    logger.info("Downloading podcast...")
    os.makedirs(output_path, exist_ok=True)
    try:
        yt = YouTube(podcast_url)
        if filename == "":
            filename = yt.title

        podcast_output_path = f"{output_path}{filename}"

        should_download: bool = True
        if os.path.exists(podcast_output_path):
            if debugging:
                should_download = False
            else:
                logger.info(f"Removing previous podcast at '{podcast_output_path}'")
                os.remove(podcast_output_path)

        if should_download:
            yt.streams.filter(progressive=True, file_extension="mp4").order_by(
                "resolution"
            )[-1].download(output_path=output_path, filename=filename)
            if not os.path.exists(podcast_output_path):
                raise DownloadError(
                    message=f"Error downloading podcast. URL: '{podcast_url}': Failed to save podcast to output path for some reason.",
                    download_type="Podcast",
                )

        return DownloadPodcastResponse(
            output_path=output_path,
            filename=filename,
            status="success",
        )
    except Exception as e:
        raise DownloadError(
            message=f"Error downloading podcast. URL: '{podcast_url}': {e}",
            download_type="Podcast",
        ) from e


def validate_string_similarity(
    string1: str, string2: str, percentage: int = 80
) -> bool:
    """
    Method to validate the similarity between two strings
    Parameters:
    - string1: str: The first string
    - string2: str: The second string
    - percentage: int: The percentage of similarity
    Returns bool: Whehter the strings are similar or not
    """

    def get_similarity_score(string1: str, string2: str) -> int:
        """
        Internal function to get similarity score
        Parameters:
        - string1: str: The first string
        - string2: str: The second string
        Returns int: The similarity score
        """
        return fuzz.token_sort_ratio(string1, string2)

    similarity_score = get_similarity_score(string1, string2)

    if (
        len(string1) > 10
        and string1 in string2
        or len(string2) > 10
        and string2 in string1
    ):
        similarity_score = 100

    is_similar_1 = get_similarity_score(string1[:10], string2) >= percentage
    is_similar_2 = get_similarity_score(string2[:10], string1) >= percentage

    if len(string1) > 10 and is_similar_1:
        return True

    if len(string2) > 10 and is_similar_2:
        return True

    if len(string1) > 20:
        if string1[:20] in string2:
            similarity_score = 100

    if len(string2) > 20:
        if string2[:20] in string1:
            similarity_score = 100

    return similarity_score >= percentage
