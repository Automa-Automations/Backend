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


class FaceFramePositionDict(TypedDict):
    frame_index: int
    face_pos_x: float
    face_pos_y: float


class MessageReturnDict(TypedDict):
    message: str
    status: Optional[str]
