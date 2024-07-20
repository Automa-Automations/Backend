from typing import Optional
from pydantic import BaseModel, field_validator
from aliases import ReturnStatus

from aliases import PodcastTranscript


class AssemblyAIParsedTranscript(BaseModel):
    sentence: str
    start_time: int
    end_time: int
    speaker: Optional[str]


class YoutubeAPITranscript(BaseModel):
    text: str
    start: float
    duration: float


class FaceFramePosition(BaseModel):
    frame_index: int
    face_pos_x: float
    face_pos_y: float


class ReturnMessage(BaseModel):
    message: str
    status: Optional[str]


class ClipShortData(BaseModel):
    test: str


class TranscriptStats(BaseModel):
    score: int
    should_make_short: bool
    feedback: str

    @field_validator("should_make_short")
    def convert_should_make_short(cls, v):
        if v.lower() == "true":
            return True
        elif v.lower() == "false":
            return False
        else:
            return v


class TranscriptFeedback(BaseModel):
    stats: TranscriptStats
    transcript: PodcastTranscript


class StatusReturn(BaseModel):
    status: ReturnStatus
    error: Optional[str] = None
    message: Optional[str] = None


class DownloadPodcastResponse(BaseModel):
    output_path: str
    filename: str
    status: ReturnStatus
