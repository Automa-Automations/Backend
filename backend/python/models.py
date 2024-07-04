from typing import TypedDict, Optional


class AssemblyAIParsedTranscriptType(TypedDict):
    sentence: str
    start_time: int
    end_time: int
    speaker: Optional[str]


class YoutubeAPITranscriptDict(TypedDict):
    text: str
    start: float
    duration: float
