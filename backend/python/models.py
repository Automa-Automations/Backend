from typing import Optional
from pydantic import BaseModel

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


class TranscriptFeedback(BaseModel):
    stats: TranscriptStats
    transcript: PodcastTranscript
