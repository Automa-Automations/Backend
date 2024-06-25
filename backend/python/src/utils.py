import sys
from src.supabase import supabase
from typing import Any, BinaryIO, Optional, Any, Union
import datetime
import json
from io import BytesIO
import traceback
import uuid
import requests


def update_value(
    table: str, line: Any, val: str, new_value: Any, line_name: str = "id"
):
    try:
        if isinstance(new_value, datetime.datetime):
            new_value = str(new_value)

        supabase.table(table).update({val: new_value}).eq(
            line_name, line
        ).execute()
    except Exception as e:
        print(e, traceback.format_exc())


def get_value(table: str, line: Any, line_name: str = "id") -> dict:
    try:
        return (
            supabase.table(table)
            .select("*")
            .eq(line_name, line)
            .execute()
            .data[0]
        )
    except Exception as e:
        print(e, traceback.format_exc())
    return {}


def insert_value(table: str, values: dict) -> Union[int, str]:
    try:
        return supabase.table(table).insert(values).execute().data[0].get("id")
    except Exception as e:
        print(e, traceback.format_exc())
    return ""


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
    filename = (
        f"{new_file_name}_{filename}_{datetime.datetime.now().timestamp()}"
    )
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
