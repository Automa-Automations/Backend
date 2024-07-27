from typing import Optional, List, TypeVar
from pydantic import BaseModel, field_validator
from aliases import ReturnStatus


class ParsedTranscript(BaseModel):
    sentence: str
    start_time: int
    end_time: int
    speaker: Optional[str]


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
        elif isinstance(v, bool):
            return v
        else:
            raise ValueError("should_make_short must be a boolean value")


class TranscriptFeedback(BaseModel):
    stats: TranscriptStats
    transcript: List[ParsedTranscript]


class StatusReturn(BaseModel):
    status: ReturnStatus
    error: Optional[str] = None
    message: Optional[str] = None


class DownloadPodcastResponse(BaseModel):
    output_path: str
    filename: str


class ShortFinalTranscript(BaseModel):
    sentences: List[str]


BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
