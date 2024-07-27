from typing import Literal, TypeAlias, Union, List
from moviepy.editor import CompositeVideoClip, VideoClip

from models import (
    ParsedTranscript,
    FaceFramePosition,
    ReturnMessage,
    TranscriptFeedback,
)

PodcastTranscript = List[ParsedTranscript]

FacePositions: TypeAlias = Union[FaceFramePosition, ReturnMessage, None]

ReturnStatus: TypeAlias = Literal["error", "success", "warning"]

VideoEditingActionType: TypeAlias = Literal[
    "process frame", "clip video", "process short"
]

VideoType: TypeAlias = Literal["short", "long video"]

MoviePyClip: TypeAlias = Union[VideoClip, CompositeVideoClip]

TranscriptFeedbackList: TypeAlias = List[TranscriptFeedback]
